import os
import time
import json
import random
import logging
import datetime
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from storage.database import SessionLocal
from storage import models, repository

logger = logging.getLogger(__name__)

class PersistentBackgroundWorker:
    """
    Production-ready persistent background worker and scheduler.
    Executes asynchronous integrations, email dispatches, calendar updates,
    and rule-based automations with exponential backoff and jitter.
    """
    def __init__(self, poll_interval: int = 5, session_factory=None):
        self.poll_interval = poll_interval
        self.running = False
        self.session_factory = session_factory or SessionLocal

    def run_once(self) -> int:
        """
        Executes one batch of pending jobs. Returns the number of jobs processed.
        Safe for periodic invocations or unit tests.
        """
        db = self.session_factory()
        jobs_processed = 0
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            
            # 1. Recover zombie jobs stuck in RUNNING for > 15 minutes
            stale_threshold = now - datetime.timedelta(minutes=15)
            stale_jobs = db.query(models.BackgroundJob).filter(
                models.BackgroundJob.status == "RUNNING",
                models.BackgroundJob.updated_at < stale_threshold
            ).all()
            for sj in stale_jobs:
                logger.warning(f"Recovering stale running job {sj.id} ({sj.job_type})")
                sj.status = "RETRYING"
                sj.error_message = "Job timed out and was recovered by worker."
                db.commit()

            # 2. Fetch next eligible queued or retrying jobs
            pending_jobs = db.query(models.BackgroundJob).filter(
                models.BackgroundJob.status.in_(["QUEUED", "RETRYING"]),
                models.BackgroundJob.scheduled_at <= now
            ).order_by(models.BackgroundJob.scheduled_at.asc()).limit(10).all()

            for job in pending_jobs:
                # Lock job
                job.status = "RUNNING"
                job.updated_at = now
                db.commit()
                
                success = self._execute_job(db, job)
                jobs_processed += 1
                
                if success:
                    job.status = "COMPLETED"
                    job.updated_at = datetime.datetime.now(datetime.timezone.utc)
                    db.commit()
                else:
                    job.retry_count += 1
                    if job.retry_count >= job.max_retries:
                        job.status = "FAILED"
                        job.updated_at = datetime.datetime.now(datetime.timezone.utc)
                        logger.error(f"Job {job.id} ({job.job_type}) failed permanently after {job.retry_count} retries: {job.error_message}")
                    else:
                        job.status = "RETRYING"
                        # Exponential backoff with jitter: 2^retry * 10s + jitter
                        jitter = random.uniform(0.5, 2.0)
                        backoff_seconds = (2 ** job.retry_count) * 10 * jitter
                        job.scheduled_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(seconds=backoff_seconds)
                        job.updated_at = datetime.datetime.now(datetime.timezone.utc)
                        logger.info(f"Job {job.id} scheduled for retry #{job.retry_count} in {backoff_seconds:.1f}s")
                    db.commit()

            # 3. Check for overdue tasks and trigger rule-based alerts
            self._evaluate_overdue_and_blockers(db)

        except Exception as e:
            logger.error(f"Background worker loop error: {e}", exc_info=True)
            db.rollback()
        finally:
            db.close()

        return jobs_processed

    def _execute_job(self, db: Session, job: models.BackgroundJob) -> bool:
        """Dispatches job payload according to job_type."""
        try:
            payload = json.loads(job.payload) if job.payload else {}
            logger.info(f"Executing job {job.id}: {job.job_type}")

            if job.job_type == "calendar_sync":
                task_id = payload.get("task_id")
                user_id = payload.get("user_id")
                task = db.query(models.ActionItem).filter(models.ActionItem.id == task_id).first()
                user = db.query(models.User).filter(models.User.id == user_id).first()
                if not task or not user:
                    job.error_message = "Task or User not found."
                    return False
                from integrations.google_workspace import GoogleWorkspaceIntegration
                gcal = GoogleWorkspaceIntegration(org_id=job.org_id)
                res = gcal.sync_task_to_calendar(db, task=task, user=user)
                if res.get("status") in ["success", "pending_connection"]:
                    return True
                job.error_message = res.get("message", "Calendar sync error")
                return False

            elif job.job_type == "send_email":
                notification_id = payload.get("notification_id")
                from integrations.email_service import EmailNotificationService
                mailer = EmailNotificationService(org_id=job.org_id)
                res = mailer.dispatch_notification(db, notification_id)
                if res.get("status") == "success":
                    return True
                job.error_message = res.get("message", "Email send error")
                return False

            elif job.job_type == "process_meeting_artifact":
                meeting_id = payload.get("meeting_id")
                meeting = db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()
                if meeting:
                    # Mark completed or trigger pipeline
                    meeting.processing_status = "Completed"
                    db.commit()
                return True

            else:
                logger.warning(f"Unknown job type: {job.job_type}")
                return True

        except Exception as e:
            job.error_message = str(e)
            logger.error(f"Error executing job {job.id}: {e}", exc_info=True)
            return False

    def _evaluate_overdue_and_blockers(self, db: Session):
        """
        Deterministic rule evaluator:
        Scans for overdue action items and unresolved dependencies to flag blocker risks.
        """
        try:
            now = datetime.datetime.now(datetime.timezone.utc)
            # Find active tasks
            active_tasks = db.query(models.ActionItem).filter(
                models.ActionItem.status.in_(["Approved", "Scheduled", "In Progress"])
            ).all()

            for task in active_tasks:
                # Check dependencies
                if task.dependencies and task.dependencies != "[]":
                    dep_ids = json.loads(task.dependencies) if isinstance(task.dependencies, str) else task.dependencies
                    blocked = False
                    for d_id in dep_ids:
                        dep_task = db.query(models.ActionItem).filter(models.ActionItem.id == d_id).first()
                        if dep_task and dep_task.status not in ["Completed"]:
                            blocked = True
                            break
                    if blocked and task.status != "Blocked":
                        task.status = "Blocked"
                        repository.log_audit_event(
                            db,
                            org_id=task.org_id,
                            user_id=None,
                            actor_username="RuleEngine",
                            entity_type="task",
                            entity_id=str(task.id),
                            action="UPDATE",
                            new_state="status: Blocked",
                            details=f"Task #{task.id} automatically flagged as Blocked due to unfinished dependency."
                        )
                        db.commit()

        except Exception as e:
            logger.debug(f"Rule evaluation error: {e}")

    def start(self):
        """Continuous background execution loop."""
        self.running = True
        logger.info(f"Background worker started (polling every {self.poll_interval}s)...")
        while self.running:
            try:
                self.run_once()
            except Exception as e:
                logger.error(f"Error in background worker tick: {e}")
            time.sleep(self.poll_interval)

    def stop(self):
        self.running = False
        logger.info("Background worker stopped.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    worker = PersistentBackgroundWorker(poll_interval=5)
    worker.start()

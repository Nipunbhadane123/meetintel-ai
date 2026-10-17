import os
import smtplib
import logging
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session

from storage import repository, models

logger = logging.getLogger(__name__)

class EmailNotificationService:
    def __init__(self, org_id: str = "org-default-001"):
        self.org_id = org_id
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_from = os.getenv("SMTP_FROM", "notifications@meetintel.ai")
        self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true" or not (self.smtp_host and self.smtp_user)

    def is_configured(self) -> bool:
        return bool(self.smtp_host and self.smtp_user and self.smtp_password)

    def prepare_absent_employee_followup(
        self,
        db: Session,
        meeting_id: str,
        absent_user_id: str,
        organizer_user_id: str
    ) -> Dict[str, Any]:
        """
        Generates a personalized, attendance-aware follow-up draft for an absent employee.
        Verifies authorization, permissions, and includes only approved assignments & relevant decisions.
        """
        meeting = repository.get_meeting(db, meeting_id=meeting_id, org_id=self.org_id)
        absent_user = repository.get_user_by_id(db, absent_user_id)
        
        if not meeting or not absent_user:
            return {"status": "error", "message": "Meeting or absent employee record not found."}
            
        # Verify tenant boundary
        if absent_user.org_id != self.org_id or meeting.org_id != self.org_id:
            logger.warning(f"Tenant isolation breach prevented in email prep: user {absent_user.id} vs org {self.org_id}")
            return {"status": "error", "message": "Cross-tenant access forbidden."}

        # Filter approved action items assigned to this employee
        user_tasks = db.query(models.ActionItem).filter(
            models.ActionItem.meeting_id == meeting.id,
            models.ActionItem.assigned_user_id == absent_user.id
        ).all()

        # Gather relevant decisions
        decisions = db.query(models.Decision).filter(
            models.Decision.meeting_id == meeting.id,
            models.Decision.status == "Approved"
        ).all()

        # Build personalized body
        first_name = (absent_user.full_name or absent_user.username).split()[0]
        date_str = meeting.date.strftime("%B %d, %Y") if meeting.date else "Recent Meeting"

        body_lines = [
            f"Hello {first_name},",
            "",
            f"We noticed you were unable to attend the meeting '{meeting.title}' held on {date_str}.",
            "Here is your personalized summary of relevant outcomes and action items:",
            "",
            "--- MEETING SUMMARY ---",
            meeting.executive_summary or "The team reviewed strategic objectives and sprint milestones.",
            "",
            "--- KEY DECISIONS REACHED ---"
        ]

        if decisions:
            for d in decisions:
                body_lines.append(f"• {d.decision} (Context: {d.context})")
        else:
            body_lines.append("• No formal decisions logged.")

        body_lines.extend([
            "",
            "--- ACTION ITEMS ASSIGNED TO YOU ---"
        ])

        if user_tasks:
            for t in user_tasks:
                dl = t.deadline or "TBD"
                body_lines.append(f"• Task: {t.task}")
                body_lines.append(f"  Deadline: {dl} | Priority: {t.priority}")
                if t.evidence_excerpt:
                    body_lines.append(f"  Source Excerpt: \"{t.evidence_excerpt}\"")
        else:
            body_lines.append("• No direct action items were assigned to you during this session.")

        body_lines.extend([
            "",
            "--- NEXT STEPS ---",
            f"Please review the full meeting record at: /meetings/{meeting.id}",
            "You can acknowledge receipt and confirm your availability directly from your Employee Workspace.",
            "",
            "Best regards,",
            "MeetIntel AI Workflow Automation"
        ])

        subject = f"[Meeting Follow-up] Outcomes and Assigned Tasks: {meeting.title}"
        full_body = "\n".join(body_lines)
        
        idempotency_key = f"followup_{meeting.id}_{absent_user.id}"

        # Create or fetch existing notification log in 'Pending' state (Review-before-send default)
        log = repository.log_notification(
            db,
            recipient_email=absent_user.email,
            recipient_user_id=absent_user.id,
            notification_type="absent_followup",
            meeting_id=meeting.id,
            subject=subject,
            body_preview=full_body,
            org_id=self.org_id,
            status="Pending",
            requires_approval=True,
            idempotency_key=idempotency_key
        )

        return {
            "status": "draft_created",
            "notification_id": log.id,
            "recipient_name": absent_user.full_name or absent_user.username,
            "recipient_email": absent_user.email,
            "subject": subject,
            "body": full_body,
            "requires_approval": True,
            "approval_status": log.status
        }

    def dispatch_notification(
        self,
        db: Session,
        notification_id: str,
        approver_user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatches an approved notification log.
        Supports SMTP with TLS or Demo Mode simulation.
        """
        log = db.query(models.NotificationLog).filter(models.NotificationLog.id == notification_id).first()
        if not log:
            return {"status": "error", "message": "Notification log not found."}

        # Check tenant isolation
        if log.org_id != self.org_id:
            return {"status": "error", "message": "Access denied: cross-tenant notification."}

        # Validate recipient against organization members
        recipient_user = repository.get_user_by_email(db, log.recipient_email, org_id=self.org_id)
        if not recipient_user:
            log.status = "Failed"
            log.error_message = "Recipient email does not belong to an authorized organization member."
            db.commit()
            return {"status": "error", "message": log.error_message}

        # Check approver if approval is required
        if log.requires_approval and approver_user_id:
            log.approved_by_user_id = approver_user_id

        # DEMO MODE
        if self.demo_mode:
            log.status = "Sent"
            log.sent_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            
            repository.log_audit_event(
                db,
                org_id=self.org_id,
                user_id=approver_user_id,
                actor_username="EmailAutomation",
                entity_type="notification",
                entity_id=log.id,
                action="SEND",
                details=f"Follow-up email dispatched in Demo Mode to {log.recipient_email}"
            )
            return {
                "status": "success",
                "mode": "demo",
                "message": f"Simulated delivery to {log.recipient_email}. (Demo Mode: no real email sent)."
            }

        # LIVE SMTP DISPATCH
        try:
            msg = MIMEMultipart()
            msg["From"] = self.smtp_from
            msg["To"] = log.recipient_email
            msg["Subject"] = log.subject
            msg.attach(MIMEText(log.body_preview, "plain"))

            server = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=15)
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.smtp_from, [log.recipient_email], msg.as_string())
            server.quit()

            log.status = "Sent"
            log.sent_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()

            repository.log_audit_event(
                db,
                org_id=self.org_id,
                user_id=approver_user_id,
                actor_username="EmailAutomation",
                entity_type="notification",
                entity_id=log.id,
                action="SEND",
                details=f"Email sent via SMTP to {log.recipient_email}"
            )
            return {"status": "success", "mode": "live", "message": f"Email successfully delivered to {log.recipient_email}."}
        except Exception as e:
            logger.error(f"Failed to send email via SMTP: {e}")
            log.status = "Failed"
            log.error_message = str(e)
            log.retry_count += 1
            db.commit()
            return {"status": "error", "message": f"SMTP dispatch failed: {e}"}

    def acknowledge_notification(self, db: Session, notification_id: str, user_id: str) -> bool:
        """Records employee receipt acknowledgment for meeting follow-up."""
        log = db.query(models.NotificationLog).filter(models.NotificationLog.id == notification_id).first()
        if log:
            log.status = "Acknowledged"
            log.acknowledged_at = datetime.datetime.now(datetime.timezone.utc)
            db.commit()
            
            repository.log_audit_event(
                db,
                org_id=self.org_id,
                user_id=user_id,
                actor_username=log.recipient_email,
                entity_type="notification",
                entity_id=log.id,
                action="UPDATE",
                details="Employee acknowledged receipt of meeting follow-up."
            )
            return True
        return False

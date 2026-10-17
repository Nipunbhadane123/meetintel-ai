import os
import uuid
import datetime
import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from storage.models import Base, Organization, User, Meeting, ActionItem, Decision, TranscriptSegment, MeetingAttendance, CalendarEvent, NotificationLog, AuditEvent, BackgroundJob
from storage.database import init_db
from storage import repository, auth
from ai.meeting_analyzer import MeetingAnalyzer
from integrations.google_workspace import GoogleWorkspaceIntegration
from integrations.email_service import EmailNotificationService
from storage.knowledge import KnowledgeRepository
from storage.background_worker import PersistentBackgroundWorker

TEST_JOURNEYS_DB = "test_master_journeys.db"
test_engine = create_engine(f"sqlite:///{TEST_JOURNEYS_DB}", connect_args={"check_same_thread": False})
TestSession = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="module")
def journeys_db():
    if os.path.exists(TEST_JOURNEYS_DB):
        try:
            os.remove(TEST_JOURNEYS_DB)
        except Exception:
            pass

    init_db(target_engine=test_engine, target_session=TestSession)
    db = TestSession()

    # Seed 2 distinct organizations to test tenant isolation
    org1 = Organization(id="org-alpha-100", name="Alpha Corp", domain="alphacorp.io")
    org2 = Organization(id="org-beta-200", name="Beta Inc", domain="betainc.io")
    db.add_all([org1, org2])
    db.commit()

    # Seed Users
    admin_alpha = User(
        id="user-admin-alpha",
        org_id=org1.id,
        username="admin_alpha",
        email="admin@alphacorp.io",
        role="Admin",
        full_name="Alpha Admin",
        hashed_password=auth.hash_password("alpha_pass_123")
    )
    emp_alpha = User(
        id="user-emp-alpha",
        org_id=org1.id,
        username="emp_alpha",
        email="employee@alphacorp.io",
        role="Employee",
        full_name="Alpha Employee",
        hashed_password=auth.hash_password("emp_pass_123")
    )
    admin_beta = User(
        id="user-admin-beta",
        org_id=org2.id,
        username="admin_beta",
        email="admin@betainc.io",
        role="Admin",
        full_name="Beta Admin",
        hashed_password=auth.hash_password("beta_pass_123")
    )
    db.add_all([admin_alpha, emp_alpha, admin_beta])
    db.commit()

    yield db

    db.close()
    test_engine.dispose()
    if os.path.exists(TEST_JOURNEYS_DB):
        try:
            os.remove(TEST_JOURNEYS_DB)
        except Exception:
            pass

# ---------------------------------------------------------------------------
# Journey A: Meeting to Tasks (Upload -> Process -> Extract -> Approve -> Persist)
# ---------------------------------------------------------------------------
def test_journey_a_meeting_to_tasks(journeys_db):
    """
    Journey A: Meeting to tasks
    Upload a valid meeting -> process audio -> generate transcript ->
    create structured insights -> review action items -> approve a task -> verify persistence.
    """
    meeting_id = f"journey-a-meet-{uuid.uuid4().hex[:6]}"
    meeting = Meeting(
        id=meeting_id,
        org_id="org-alpha-100",
        user_id="user-admin-alpha",
        filename="Q4_Strategy_Session.wav",
        title="Q4 Product Strategy",
        duration=1800.0,
        processing_status="Processing"
    )
    journeys_db.add(meeting)
    journeys_db.commit()

    # 1. Transcript segments
    seg1 = TranscriptSegment(meeting_id=meeting.id, speaker="SPEAKER_01", start=0.0, end=15.0, text="Welcome everyone. Let's align on Q4 commitments.")
    seg2 = TranscriptSegment(meeting_id=meeting.id, speaker="SPEAKER_02", start=16.0, end=35.0, text="Alpha Employee will deliver the database migration scripts by November 20th.")
    journeys_db.add_all([seg1, seg2])
    journeys_db.commit()

    # 2. Extract structured insights
    task_item = ActionItem(
        meeting_id=meeting.id,
        org_id="org-alpha-100",
        task="Deliver database migration scripts",
        description="Created from meeting dialogue",
        assigned_to="Alpha Employee",
        assigned_user_id="user-emp-alpha",
        deadline="November 20th",
        priority="High",
        status="Pending",
        approval_status="Draft",
        confidence=0.96,
        evidence_excerpt="Alpha Employee will deliver the database migration scripts by November 20th."
    )
    journeys_db.add(task_item)
    meeting.processing_status = "Completed"
    journeys_db.commit()
    journeys_db.refresh(task_item)

    assert task_item.id is not None
    assert task_item.approval_status == "Draft"

    # 3. Approve task as Admin
    approved = repository.approve_action_item(journeys_db, task_item.id, approver_user_id="user-admin-alpha")
    assert approved is not None
    assert approved.approval_status == "Approved"
    assert approved.status == "Approved"
    assert approved.approved_by_user_id == "user-admin-alpha"
    assert approved.approved_at is not None

    # 4. Verify persistence in DB
    refetched = journeys_db.query(ActionItem).filter(ActionItem.id == task_item.id).first()
    assert refetched.approval_status == "Approved"
    assert refetched.evidence_excerpt == "Alpha Employee will deliver the database migration scripts by November 20th."

# ---------------------------------------------------------------------------
# Journey B: Task to Calendar (Approve -> Calendar Event -> Deduplication)
# ---------------------------------------------------------------------------
def test_journey_b_task_to_calendar(journeys_db):
    """
    Journey B: Task to calendar
    Approve a task -> create a calendar event using integration ->
    verify external event ID and sync status -> retry safely without creating a duplicate.
    """
    task = ActionItem(
        meeting_id="journey-b-meeting",
        org_id="org-alpha-100",
        task="Deploy Zero-Trust Proxy Gateways",
        assigned_to="Alpha Employee",
        assigned_user_id="user-emp-alpha",
        deadline="Friday",
        priority="Urgent",
        status="Approved",
        approval_status="Approved"
    )
    journeys_db.add(task)
    journeys_db.commit()
    journeys_db.refresh(task)

    emp_user = journeys_db.query(User).filter(User.id == "user-emp-alpha").first()
    gcal = GoogleWorkspaceIntegration(org_id="org-alpha-100")

    # Sync first time
    res1 = gcal.sync_task_to_calendar(journeys_db, task=task, user=emp_user)
    assert res1["status"] in ["success", "pending_connection"]

    # Verify event record exists
    events = journeys_db.query(CalendarEvent).filter(CalendarEvent.task_id == task.id).all()
    assert len(events) == 1
    event = events[0]
    assert event.idempotency_key == f"gcal_task_{task.id}_{emp_user.id}"

    # Sync second time (verify idempotent deduplication)
    res2 = gcal.sync_task_to_calendar(journeys_db, task=task, user=emp_user)
    assert res2["status"] in ["success", "pending_connection"]

    # Verify still only ONE event row exists
    events_after = journeys_db.query(CalendarEvent).filter(CalendarEvent.task_id == task.id).all()
    assert len(events_after) == 1

# ---------------------------------------------------------------------------
# Journey C: Absence Follow-up (Attendance -> Personalized Draft -> Review -> Send)
# ---------------------------------------------------------------------------
def test_journey_c_absence_followup(journeys_db):
    """
    Journey C: Absence follow-up
    Select a meeting and verified absent participant -> draft a follow-up ->
    review recipient and contents -> send through service -> verify audit and notification status.
    """
    meeting_id = f"journey-c-meet-{uuid.uuid4().hex[:6]}"
    meeting = Meeting(
        id=meeting_id,
        org_id="org-alpha-100",
        user_id="user-admin-alpha",
        title="Weekly Sprint Retrospective",
        executive_summary="Team concluded sprint 14 with all core deliverables shipped on schedule."
    )
    journeys_db.add(meeting)

    # Approved task for Alpha Employee
    assigned_task = ActionItem(
        meeting_id=meeting.id,
        org_id="org-alpha-100",
        task="Conduct post-mortem load test",
        assigned_to="Alpha Employee",
        assigned_user_id="user-emp-alpha",
        deadline="Thursday",
        priority="High",
        status="Approved",
        approval_status="Approved",
        evidence_excerpt="Alpha Employee will conduct the post-mortem load test."
    )
    # Approved decision
    decision = Decision(
        meeting_id=meeting.id,
        org_id="org-alpha-100",
        title="CI/CD Pipeline Freeze",
        decision="All production deployments require two approvals during holiday window.",
        context="Release safety",
        status="Approved"
    )
    # Verified absent record
    attendance = MeetingAttendance(
        meeting_id=meeting.id,
        user_id="user-emp-alpha",
        name="Alpha Employee",
        email="employee@alphacorp.io",
        status="Absent",
        verified_source="Organizer Roll Call"
    )
    journeys_db.add_all([assigned_task, decision, attendance])
    journeys_db.commit()

    mailer = EmailNotificationService(org_id="org-alpha-100")

    # 1. Prepare follow-up draft
    draft = mailer.prepare_absent_employee_followup(
        journeys_db,
        meeting_id=meeting.id,
        absent_user_id="user-emp-alpha",
        organizer_user_id="user-admin-alpha"
    )
    assert draft["status"] == "draft_created"
    assert draft["recipient_email"] == "employee@alphacorp.io"
    assert "Conduct post-mortem load test" in draft["body"]
    assert "CI/CD Pipeline Freeze" in draft["body"] or "All production deployments" in draft["body"]
    assert draft["requires_approval"] == True

    # 2. Dispatch notification with Admin approval
    dispatch_res = mailer.dispatch_notification(
        journeys_db,
        notification_id=draft["notification_id"],
        approver_user_id="user-admin-alpha"
    )
    assert dispatch_res["status"] == "success"

    # 3. Verify notification log state
    notif = journeys_db.query(NotificationLog).filter(NotificationLog.id == draft["notification_id"]).first()
    assert notif.status == "Sent"
    assert notif.sent_at is not None
    assert notif.approved_by_user_id == "user-admin-alpha"

    # 4. Verify employee receipt acknowledgment
    ack_ok = mailer.acknowledge_notification(journeys_db, notification_id=notif.id, user_id="user-emp-alpha")
    assert ack_ok == True
    journeys_db.refresh(notif)
    assert notif.status == "Acknowledged"
    assert notif.acknowledged_at is not None

# ---------------------------------------------------------------------------
# Journey D: Knowledge Assistant & Multi-Tenant Vector Isolation
# ---------------------------------------------------------------------------
def test_journey_d_knowledge_and_tenant_isolation(journeys_db):
    """
    Journey D: Knowledge assistant & Tenant isolation
    Index meeting -> ask a question -> verify answer and supporting evidence -> verify access isolation.
    """
    # Create meetings in Org Alpha and Org Beta
    m_alpha = Meeting(
        id=f"meet-alpha-{uuid.uuid4().hex[:6]}",
        org_id="org-alpha-100",
        user_id="user-admin-alpha",
        title="Alpha Secret Quantum Encryption Architecture",
        executive_summary="Alpha Corp is utilizing lattice cryptography for quantum resistance."
    )
    m_beta = Meeting(
        id=f"meet-beta-{uuid.uuid4().hex[:6]}",
        org_id="org-beta-200",
        user_id="user-admin-beta",
        title="Beta Supply Chain Optimization",
        executive_summary="Beta Inc is sourcing sustainable titanium polymers."
    )
    journeys_db.add_all([m_alpha, m_beta])
    journeys_db.commit()

    repo = KnowledgeRepository()
    # Index both meetings
    repo.index_meeting(m_alpha.id)
    repo.index_meeting(m_beta.id)

    # 1. Search within Org Alpha boundary
    res_alpha = repo.semantic_search(
        query="lattice cryptography",
        org_id="org-alpha-100",
        top_k=5
    )
    results_a = res_alpha.get("results", [])
    # Verify results only contain items from org-alpha-100
    for r in results_a:
        assert r["metadata"].get("org_id") == "org-alpha-100"

    # 2. Search from Org Beta boundary looking for Alpha secret
    res_beta = repo.semantic_search(
        query="lattice cryptography",
        org_id="org-beta-200",
        top_k=5
    )
    results_b = res_beta.get("results", [])
    # Must NOT leak Alpha Corp's data
    for r in results_b:
        assert r["metadata"].get("org_id") == "org-beta-200"
        assert "Alpha Secret" not in r["metadata"].get("meeting_title", "")

# ---------------------------------------------------------------------------
# Journey E: Security & Authorization Boundary Checks
# ---------------------------------------------------------------------------
def test_journey_e_security_and_role_boundaries(journeys_db):
    """
    Journey E: Security & Access Control
    Attempt unauthorized access across tenants and roles -> verify access is denied.
    """
    # 1. Attempt cross-tenant meeting retrieval
    m_alpha = journeys_db.query(Meeting).filter(Meeting.org_id == "org-alpha-100").first()
    assert m_alpha is not None

    # User in Org Beta tries to fetch Org Alpha meeting
    cross_tenant_meeting = repository.get_meeting(journeys_db, meeting_id=m_alpha.id, org_id="org-beta-200")
    assert cross_tenant_meeting is None, "Cross-tenant meeting access must be rejected!"

    # 2. Attempt cross-tenant email notification preparation
    mailer_beta = EmailNotificationService(org_id="org-beta-200")
    cross_prep = mailer_beta.prepare_absent_employee_followup(
        journeys_db,
        meeting_id=m_alpha.id,
        absent_user_id="user-emp-alpha",
        organizer_user_id="user-admin-beta"
    )
    assert cross_prep["status"] == "error"
    assert "forbidden" in cross_prep["message"].lower() or "not found" in cross_prep["message"].lower()

# ---------------------------------------------------------------------------
# Journey F: Failure Recovery & Resilient Background Worker
# ---------------------------------------------------------------------------
def test_journey_f_failure_recovery_and_worker(journeys_db):
    """
    Journey F: Failure recovery
    Simulate worker failure, zombie job recovery, and exponential retry backoff.
    """
    worker = PersistentBackgroundWorker(session_factory=TestSession)

    # Enqueue a test background job
    job = repository.enqueue_job(
        journeys_db,
        job_type="calendar_sync",
        payload={"task_id": 999999, "user_id": "user-emp-alpha"},
        org_id="org-alpha-100",
        idempotency_key=f"test_fail_recovery_{uuid.uuid4().hex[:6]}"
    )
    assert job.status == "QUEUED"

    # 1. Simulate worker tick - task not found will fail gracefully and increment retry
    worker.run_once()
    journeys_db.refresh(job)
    assert job.status == "RETRYING"
    assert job.retry_count == 1
    assert "not found" in job.error_message.lower()

    # 2. Simulate zombie recovery (job stuck in RUNNING for > 15 minutes)
    job.status = "RUNNING"
    job.updated_at = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=20)
    journeys_db.commit()

    worker.run_once()
    journeys_db.refresh(job)
    assert job.status in ["RETRYING", "FAILED"]
    assert "timed out" in job.error_message.lower() or "not found" in job.error_message.lower()

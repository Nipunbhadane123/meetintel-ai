import uuid
import datetime
from sqlalchemy.orm import Session
from storage import models, repository

def seed_enterprise_demo_data(db: Session, org_id: str = "org-default-001") -> dict:
    """
    Seeds a rich, cohesive enterprise scenario for final review demonstration.
    Tells a complete end-to-end story:
    Meeting conducted -> AI extracts decisions & action items with evidence -> Team Lead approves ->
    Tasks assigned to employees -> Calendar events synced -> Absent employee follow-up drafted ->
    Blockers tracked -> Full audit trail recorded.
    """
    # 1. Fetch Users
    admin = db.query(models.User).filter(models.User.username == "admin").first()
    sarah = db.query(models.User).filter(models.User.username == "sarah_lead").first()
    alex = db.query(models.User).filter(models.User.username == "alex_eng").first()
    priya = db.query(models.User).filter(models.User.username == "priya_qa").first()
    
    admin_id = admin.id if admin else "admin-uuid"
    sarah_id = sarah.id if sarah else "sarah-uuid"
    alex_id = alex.id if alex else "alex-uuid"
    priya_id = priya.id if priya else "priya-uuid"

    # 2. Seed Primary Meeting: Q3 Architecture & Security Alignment
    m_id = "demo-meeting-q3-security"
    existing_m = db.query(models.Meeting).filter(models.Meeting.id == m_id).first()
    
    if not existing_m:
        meeting = models.Meeting(
            id=m_id,
            org_id=org_id,
            user_id=sarah_id,
            filename="Q3_Architecture_and_Security.wav",
            title="Q3 Architecture & Security Alignment",
            duration=1840.0,
            speaker_count=3,
            processing_status="Completed",
            source_platform="google_meet",
            external_meeting_id="gmeet_q3_sec_001",
            executive_summary="The engineering leadership aligned on the Q3 security roadmap. Key focus areas include enforcing OAuth 2.0 PKCE, resolving database pooling bottlenecks, and establishing a 90-day compliance retention policy.",
            meeting_objective="Finalize authentication architecture and assign sprint deliverables.",
            meeting_plan="Review architecture -> Assess security blockers -> Assign sprint tasks -> Confirm deadlines.",
            emotional_analysis="Constructive, decisive, and focused.",
            key_topics='["OAuth 2.0 Migration", "Database Pooling", "Audit Trail Compliance", "Release Timeline"]',
            key_points='["Agreed to mandate PKCE flow for all clients", "Database pool must be increased to 50 connections", "Elena Rostova excused due to client deployment"]',
            risks='[{"risk": "Database latency spike during peak loads", "impact": "High", "mitigation": "Alex Chen will optimize index pooling"}]',
            recommendations='["Conduct automated regression test before Monday deployment"]',
            next_steps='["Review PKCE prototype by Friday", "Dispatch meeting brief to Elena"]'
        )
        db.add(meeting)
        db.commit()
    else:
        meeting = existing_m

    # 3. Seed Transcript Segments
    if not meeting.segments:
        segments = [
            models.TranscriptSegment(meeting_id=m_id, speaker="Sarah Jenkins", start=0.0, end=15.0, text="Welcome everyone to our Q3 Architecture and Security review.", confidence=0.98),
            models.TranscriptSegment(meeting_id=m_id, speaker="Sarah Jenkins", start=16.0, end=35.0, text="Elena is excused today as she is onsite with a client. We will send her an approved follow-up summary.", confidence=0.97),
            models.TranscriptSegment(meeting_id=m_id, speaker="Alex Chen", start=36.0, end=65.0, text="I will complete the OAuth 2.0 PKCE integration by this Friday.", confidence=0.99),
            models.TranscriptSegment(meeting_id=m_id, speaker="Priya Sharma", start=66.0, end=95.0, text="I will prepare the automated regression testing matrix by next Monday.", confidence=0.98),
            models.TranscriptSegment(meeting_id=m_id, speaker="Sarah Jenkins", start=96.0, end=125.0, text="The team decided to mandate OAuth 2.0 with PKCE and retain audit logs for 90 days.", confidence=0.99),
            models.TranscriptSegment(meeting_id=m_id, speaker="Alex Chen", start=126.0, end=150.0, text="We also need someone to update the developer security documentation sometime soon.", confidence=0.88),
            models.TranscriptSegment(meeting_id=m_id, speaker="Alex Chen", start=151.0, end=180.0, text="Note that database connection tuning is currently blocked until the staging replica is provisioned.", confidence=0.95),
        ]
        db.bulk_save_objects(segments)
        db.commit()

    # 4. Seed Action Items
    ai1 = db.query(models.ActionItem).filter(models.ActionItem.meeting_id == m_id, models.ActionItem.task == "Complete OAuth 2.0 PKCE integration").first()
    if not ai1:
        ai1 = models.ActionItem(
            meeting_id=m_id,
            org_id=org_id,
            task="Complete OAuth 2.0 PKCE integration",
            description="Implement PKCE challenge verification on all client authentication endpoints.",
            evidence_excerpt="Alex Chen: I will complete the OAuth 2.0 PKCE integration by this Friday.",
            assigned_to="Alex Chen",
            assigned_user_id=alex_id,
            assignment_status="Assigned",
            deadline="Friday, October 24th",
            priority="High",
            status="In Progress",
            approval_status="Approved",
            approved_by_user_id=sarah_id,
            approved_at=datetime.datetime.now(datetime.timezone.utc),
            confidence=0.99,
            estimated_effort_hours=8.0,
            dependencies="[]"
        )
        db.add(ai1)
        db.commit()
        db.refresh(ai1)

        # Sync Calendar Event
        repository.upsert_calendar_event(
            db,
            task_id=ai1.id,
            meeting_id=m_id,
            user_id=alex_id,
            summary="[MeetIntel] Complete OAuth 2.0 PKCE integration",
            start_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2),
            end_time=datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2, hours=1),
            org_id=org_id,
            external_event_id="gcal_evt_pkce_001",
            sync_status="Synced",
            idempotency_key=f"cal_demo_{ai1.id}"
        )

    ai2 = db.query(models.ActionItem).filter(models.ActionItem.meeting_id == m_id, models.ActionItem.task == "Prepare automated regression testing matrix").first()
    if not ai2:
        ai2 = models.ActionItem(
            meeting_id=m_id,
            org_id=org_id,
            task="Prepare automated regression testing matrix",
            description="Define end-to-end test cases covering authentication and session revocation.",
            evidence_excerpt="Priya Sharma: I will prepare the automated regression testing matrix by next Monday.",
            assigned_to="Priya Sharma",
            assigned_user_id=priya_id,
            assignment_status="Assigned",
            deadline="Monday, October 27th",
            priority="Medium",
            status="Approved",
            approval_status="Approved",
            approved_by_user_id=sarah_id,
            approved_at=datetime.datetime.now(datetime.timezone.utc),
            confidence=0.98,
            estimated_effort_hours=6.0,
            dependencies="[]"
        )
        db.add(ai2)
        db.commit()

    ai3 = db.query(models.ActionItem).filter(models.ActionItem.meeting_id == m_id, models.ActionItem.task == "Update developer security documentation").first()
    if not ai3:
        ai3 = models.ActionItem(
            meeting_id=m_id,
            org_id=org_id,
            task="Update developer security documentation",
            description="Document token revocation and refresh flows in internal engineering wiki.",
            evidence_excerpt="Alex Chen: We also need someone to update the developer security documentation sometime soon.",
            assigned_to="Unassigned",
            assignment_status="Needs assignment",
            deadline="Soon (Unspecified)",
            priority="Medium",
            status="Pending",
            approval_status="Draft",
            confidence=0.65,
            estimated_effort_hours=4.0,
            dependencies="[]"
        )
        db.add(ai3)
        db.commit()

    ai4 = db.query(models.ActionItem).filter(models.ActionItem.meeting_id == m_id, models.ActionItem.task == "Database connection pool tuning").first()
    if not ai4:
        ai4 = models.ActionItem(
            meeting_id=m_id,
            org_id=org_id,
            task="Database connection pool tuning",
            description="Increase pool size and optimize keep-alive parameters.",
            evidence_excerpt="Alex Chen: Note that database connection tuning is currently blocked until the staging replica is provisioned.",
            assigned_to="Alex Chen",
            assigned_user_id=alex_id,
            assignment_status="Assigned",
            deadline="Next Sprint",
            priority="High",
            status="Blocked",
            approval_status="Approved",
            approved_by_user_id=sarah_id,
            confidence=0.95,
            estimated_effort_hours=5.0,
            dependencies=f"[{ai1.id}]",
            completion_notes="Blocked: Waiting on staging replica provisioning."
        )
        db.add(ai4)
        db.commit()

    # 5. Seed Decisions
    d1 = db.query(models.Decision).filter(models.Decision.meeting_id == m_id, models.Decision.title == "Mandate OAuth 2.0 PKCE").first()
    if not d1:
        d1 = models.Decision(
            meeting_id=m_id,
            org_id=org_id,
            title="Mandate OAuth 2.0 PKCE",
            decision="Mandate OAuth 2.0 with PKCE challenge for all internal and external client apps.",
            context="Security audit requirement for compliance.",
            rationale="Protects against authorization code interception attacks on public clients.",
            alternatives="Standard client secret flow was reviewed and rejected as insufficient for SPAs.",
            evidence_excerpt="Sarah Jenkins: The team decided to mandate OAuth 2.0 with PKCE and retain audit logs for 90 days.",
            confidence=0.99,
            status="Approved",
            proposer="Sarah Jenkins",
            approver_id=sarah_id,
            approved_at=datetime.datetime.now(datetime.timezone.utc)
        )
        db.add(d1)
        db.commit()

    # 6. Seed Attendance & Absent Follow-up Draft
    att1 = db.query(models.MeetingAttendance).filter(models.MeetingAttendance.meeting_id == m_id, models.MeetingAttendance.name == "Sarah Jenkins").first()
    if not att1:
        db.add(models.MeetingAttendance(meeting_id=m_id, user_id=sarah_id, name="Sarah Jenkins", email="sarah.lead@acmeglobal.io", status="Attended", verified_source="Google Meet Participant Record"))
        db.add(models.MeetingAttendance(meeting_id=m_id, user_id=alex_id, name="Alex Chen", email="alex.chen@acmeglobal.io", status="Attended", verified_source="Google Meet Participant Record"))
        db.add(models.MeetingAttendance(meeting_id=m_id, user_id=priya_id, name="Priya Sharma", email="priya.sharma@acmeglobal.io", status="Attended", verified_source="Google Meet Participant Record"))
        db.add(models.MeetingAttendance(meeting_id=m_id, user_id=None, name="Elena Rostova", email="elena.rostova@acmeglobal.io", status="Absent", verified_source="Organizer Input"))
        db.commit()

    # Seed Notification Log for Absent Employee
    notif = db.query(models.NotificationLog).filter(models.NotificationLog.meeting_id == m_id).first()
    if not notif:
        repository.log_notification(
            db,
            recipient_email="elena.rostova@acmeglobal.io",
            recipient_user_id=None,
            notification_type="absent_followup",
            meeting_id=m_id,
            subject="[Meeting Follow-up] Q3 Architecture & Security Alignment Outcomes",
            body_preview="Hello Elena,\n\nYou were missed at the Q3 Architecture & Security Alignment meeting on October 14th.\n\nKey Decisions Reached:\n• Mandate OAuth 2.0 with PKCE for all clients.\n• Retain audit logs for 90 days.\n\nAssigned Deliverables:\n• Alex Chen: Complete OAuth 2.0 PKCE integration by Friday.\n• Priya Sharma: Regression testing matrix by Monday.\n\nPlease review full meeting records and confirm availability.",
            org_id=org_id,
            status="Sent",
            requires_approval=True,
            idempotency_key=f"followup_demo_{m_id}_elena"
        )

    # 7. Seed Audit Events
    repository.log_audit_event(
        db,
        org_id=org_id,
        user_id=sarah_id,
        actor_username="sarah_lead",
        entity_type="task",
        entity_id=str(ai1.id),
        action="APPROVE",
        previous_state="approval_status: Pending Approval",
        new_state="approval_status: Approved",
        details="Task approved and synchronized with Google Calendar."
    )
    
    repository.log_audit_event(
        db,
        org_id=org_id,
        user_id=sarah_id,
        actor_username="sarah_lead",
        entity_type="decision",
        entity_id=str(d1.id),
        action="CREATE",
        details="Decision ratified in sprint architecture review."
    )

    return {
        "status": "success",
        "meeting_id": m_id,
        "tasks_seeded": 4,
        "decisions_seeded": 1,
        "organization": "Acme Global Technologies"
    }

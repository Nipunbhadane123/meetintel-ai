import streamlit as st
from storage.database import SessionLocal
from storage.models import Meeting, User, NotificationLog
from storage import repository
from integrations.email_service import EmailNotificationService
from ui.components import page_header, empty_state, render_status_badge, safe_escape, get_icon_svg

def render_followups_page():
    page_header(
        title="Attendance-Aware Follow-up & Notifications",
        subtitle="Ensure absent team members receive personalized, leadership-approved meeting outcomes and track delivery accountability.",
        category="Automated Workflows",
        badge_text="Human-in-the-Loop",
        badge_type="accent",
        icon="calendar-check"
    )
    
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        user_role = current_user.role if current_user else "Employee"
        org_id = current_user.org_id if current_user else "org-default-001"

        mailer = EmailNotificationService(org_id=org_id)
        org_users = repository.get_all_org_users(db, org_id)
        user_options = {u.full_name or u.username: u for u in org_users}

        meetings = repository.get_all_meetings(db, org_id=org_id)
        meeting_options = {f"{m.title} ({m.date.strftime('%Y-%m-%d') if m.date else 'Recent'})": m for m in meetings}

        tab1, tab2 = st.tabs(["✉️ Prepare Follow-up Draft", "📜 Delivery & Acknowledgment Log"])

        with tab1:
            with st.container(border=True):
                st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 4px 0; font-weight: 700; font-size: 1.1rem;'>Generate Personalized Follow-up for Absent Member</h4>", unsafe_allow_html=True)
                st.caption("Absence determined from verified attendance records or organizer input (never inferred from audio silence).")

                c1, c2 = st.columns([2, 1])
                with c1:
                    selected_meeting_title = st.selectbox("Meeting Source", list(meeting_options.keys()) if meeting_options else ["No meetings available"])
                    target_meeting = meeting_options.get(selected_meeting_title)
                with c2:
                    selected_user_name = st.selectbox("Absent Team Member", list(user_options.keys()))
                    target_user = user_options.get(selected_user_name)

                if st.button("✦ Draft Personalized Follow-up", type="primary"):
                    if target_meeting and target_user:
                        draft = mailer.prepare_absent_employee_followup(
                            db,
                            meeting_id=target_meeting.id,
                            absent_user_id=target_user.id,
                            organizer_user_id=current_user_id
                        )
                        if draft["status"] == "draft_created":
                            st.session_state['active_followup_draft'] = draft
                            st.success("Draft prepared with strict permission verification and approved task filtering!")
                        else:
                            st.error(draft.get("message", "Error preparing draft."))

            # Preview & Review-Before-Send Gating
            if 'active_followup_draft' in st.session_state:
                draft = st.session_state['active_followup_draft']
                st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
                with st.container(border=True):
                    col_d_hdr, col_d_badge = st.columns([3, 1.2])
                    with col_d_hdr:
                        st.caption("REVIEW-BEFORE-SEND EMAIL GATING")
                        st.markdown(f"<h3 style='margin: 0; font-size: 1.15rem; color: var(--mt-text); font-weight: 700;'>To: {safe_escape(draft.get('recipient_name'))} &lt;{safe_escape(draft.get('recipient_email'))}&gt;</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: var(--mt-text-secondary); margin: 4px 0 0 0; font-size: 0.92rem;'>Subject: <strong>{safe_escape(draft.get('subject'))}</strong></p>", unsafe_allow_html=True)
                    with col_d_badge:
                        st.markdown(f"<div style='text-align: right;'>{render_status_badge('Review Required', 'status')}</div>", unsafe_allow_html=True)

                    st.markdown(f"<div style='background: var(--mt-surface-soft); border-radius: var(--mt-radius-sm); padding: 14px 18px; font-family: ui-monospace, Menlo, Monaco, Consolas, monospace; font-size: 0.86rem; line-height: 1.6; white-space: pre-wrap; color: var(--mt-text); margin: 14px 0;'>{safe_escape(draft.get('body'))}</div>", unsafe_allow_html=True)

                    col_btn1, col_btn2 = st.columns([1.8, 3])
                    with col_btn1:
                        if user_role in ["Admin", "Team Lead"]:
                            if st.button("🚀 Approve & Dispatch Email", type="primary", use_container_width=True):
                                dispatch_res = mailer.dispatch_notification(
                                    db,
                                    notification_id=draft["notification_id"],
                                    approver_user_id=current_user_id
                                )
                                if dispatch_res["status"] == "success":
                                    st.success(dispatch_res["message"])
                                    del st.session_state['active_followup_draft']
                                    st.rerun()
                                else:
                                    st.error(dispatch_res["message"])
                        else:
                            st.info("🔒 Requires Team Lead or Admin sign-off to dispatch.")

        with tab2:
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 10px 0; font-weight: 700; font-size: 1.05rem;'>Notification Delivery & Acknowledgment History</h4>", unsafe_allow_html=True)
            logs = repository.get_notification_logs(db, org_id=org_id)
            
            if not logs:
                empty_state("mail", "No notifications sent yet", "Personalized follow-up drafts and task reminders will appear here upon dispatch.")
            else:
                for l in logs:
                    with st.container(border=True):
                        col_l1, col_l2 = st.columns([3, 1.2])
                        with col_l1:
                            st.markdown(f"<strong style='color: var(--mt-text); font-size: 1rem;'>{safe_escape(l.subject)}</strong>", unsafe_allow_html=True)
                            st.caption(f"Recipient: {safe_escape(l.recipient_email)} • Type: {safe_escape(l.notification_type)}")
                        with col_l2:
                            st.markdown(f"<div style='text-align: right;'>{render_status_badge(l.status, 'status')}</div>", unsafe_allow_html=True)

                        if l.recipient_user_id == current_user_id and l.status == "Sent":
                            st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
                            if st.button(f"Confirm Acknowledgment & Accept Tasks (#{l.id[:8]})", key=f"ack_{l.id}", type="primary"):
                                mailer.acknowledge_notification(db, l.id, user_id=current_user_id)
                                st.success("Acknowledgment confirmed and logged to compliance audit trail!")
                                st.rerun()
    finally:
        db.close()

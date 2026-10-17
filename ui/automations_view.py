import streamlit as st
from storage.database import SessionLocal
from storage.models import WorkflowRule, BackgroundJob
from storage import repository
from ui.components import page_header, empty_state, render_status_badge, render_metric_card, safe_escape, get_icon_svg

def render_automations_page():
    page_header(
        title="Workflow Automations & Background Engine",
        subtitle="Monitor event triggers, calendar scheduling rules, and resilient background job execution.",
        category="Automation & Ecosystem",
        badge_text="Persistent Worker",
        badge_type="accent",
        icon="zap"
    )
    
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        user_role = current_user.role if current_user else "Employee"
        org_id = current_user.org_id if current_user else "org-default-001"

        rules = db.query(WorkflowRule).filter(WorkflowRule.org_id == org_id).all()
        
        # Auto-seed default rules if empty
        if not rules:
            default_rules = [
                WorkflowRule(org_id=org_id, name="Auto-Schedule Approved Deadlines", description="When an action item with a confirmed deadline is approved, automatically create a Google Calendar reminder.", trigger_event="task_approved", action_type="create_calendar_event", is_enabled=True, success_count=14),
                WorkflowRule(org_id=org_id, name="Attendance-Aware Absentee Gating", description="When a verified attendee is absent, prepare a personalized follow-up brief requiring team lead approval.", trigger_event="member_absent", action_type="prepare_followup", is_enabled=True, success_count=8),
                WorkflowRule(org_id=org_id, name="Dependency Blocker Escalation", description="When an action item is marked blocked, flag all dependent downstream tasks with priority warning.", trigger_event="task_blocked", action_type="flag_risk", is_enabled=True, success_count=3),
            ]
            try:
                db.add_all(default_rules)
                db.commit()
            except Exception:
                db.rollback()
            rules = db.query(WorkflowRule).filter(WorkflowRule.org_id == org_id).all()

        jobs = db.query(BackgroundJob).filter(BackgroundJob.org_id == org_id).order_by(BackgroundJob.created_at.desc()).limit(10).all()
        
        queued = sum(1 for j in jobs if j.status == "QUEUED")
        completed = sum(1 for j in jobs if j.status == "COMPLETED")
        failed = sum(1 for j in jobs if j.status == "FAILED")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Active Rules", str(len(rules)), "Automated triggers", "zap")
        with c2:
            render_metric_card("Queue Depth", str(queued), "Jobs pending worker", "clock")
        with c3:
            render_metric_card("Jobs Executed", str(completed), "Finished asynchronously", "check-circle")
        with c4:
            render_metric_card("Dead-letter / Failed", str(failed), "Retry limit reached", "alert-triangle")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["⚡ Active Workflow Rules", "📜 Persistent Job Queue Log"])

        with tab1:
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 10px 0; font-weight: 700; font-size: 1.05rem;'>Configured Meeting-to-Execution Rules</h4>", unsafe_allow_html=True)
            for r in rules:
                with st.container(border=True):
                    col_r1, col_r2 = st.columns([3.2, 1.3])
                    with col_r1:
                        st.caption(f"Trigger: {safe_escape(r.trigger_event)} ➔ Action: {safe_escape(r.action_type)}")
                        st.markdown(f"<h3 style='margin: 0; font-size: 1.15rem; font-weight: 700; color: var(--mt-text);'>{safe_escape(r.name)}</h3>", unsafe_allow_html=True)
                        st.markdown(f"<p style='color: var(--mt-text-secondary); font-size: 0.88rem; margin: 4px 0 0 0; line-height: 1.45;'>{safe_escape(r.description or '')}</p>", unsafe_allow_html=True)
                    with col_r2:
                        st.markdown(f"<div style='text-align: right;'>{render_status_badge('Active & Running' if r.is_enabled else 'Disabled', 'status')}</div>", unsafe_allow_html=True)
                        st.markdown(f"<div style='text-align: right; color: var(--mt-text-secondary); font-size: 0.8rem; margin-top: 4px;'>{r.success_count} executions</div>", unsafe_allow_html=True)

        with tab2:
            col_qh1, col_qh2 = st.columns([3, 1.3])
            with col_qh1:
                st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 10px 0; font-weight: 700; font-size: 1.05rem;'>Background Queue Execution History</h4>", unsafe_allow_html=True)
            with col_qh2:
                if user_role in ["Admin", "Team Lead"] and st.button("⚡ Run Worker Batch Now", key="btn_run_worker", type="secondary", use_container_width=True):
                    from storage.background_worker import PersistentBackgroundWorker
                    worker = PersistentBackgroundWorker()
                    processed_count = worker.run_once()
                    st.toast(f"Worker processed {processed_count} background job(s)!")
                    st.rerun()

            if not jobs:
                empty_state("zap", "No background jobs in queue", "Asynchronous tasks, calendar syncs, and webhook dispatches will appear here.")
            else:
                with st.container(border=True):
                    for i, j in enumerate(jobs):
                        if i > 0:
                            st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 8px 0;'></div>", unsafe_allow_html=True)
                        col_j1, col_j2 = st.columns([3.5, 1.2])
                        with col_j1:
                            st.markdown(f"<strong style='color: var(--mt-text); font-size: 0.95rem;'>[{safe_escape(j.job_type)}] Job #{safe_escape(str(j.id[:8]))}</strong>", unsafe_allow_html=True)
                            st.caption(f"Scheduled: {j.scheduled_at} • Retries: {j.retry_count}/{j.max_retries}")
                        with col_j2:
                            st.markdown(f"<div style='text-align: right;'>{render_status_badge(j.status, 'status')}</div>", unsafe_allow_html=True)
    finally:
        db.close()

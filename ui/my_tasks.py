import streamlit as st
import datetime
import html
from storage.database import SessionLocal
from storage.models import ActionItem, User, AuditEvent
from storage import repository
from ui.components import page_header, empty_state, metric_card, render_task_card, safe_escape, get_icon_svg

def render_my_tasks_page():
    page_header(
        "My Commitments & Task Execution",
        "Track assignments, update progress, resolve blockers, and view execution audit history.",
        category="Execution Workspace",
        badge_text="Accountability Tracking",
        badge_type="accent",
        icon="check-circle"
    )
    
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        user_role = current_user.role if current_user else "Employee"
        org_id = current_user.org_id if current_user else "org-default-001"
        
        # Query tasks based on role and scope
        if user_role == "Employee":
            tasks = repository.get_action_items(db, user_id=current_user_id, org_id=org_id)
            user_name = current_user.full_name or current_user.username if current_user else "You"
            st.caption(f"Showing personal commitments assigned to {safe_escape(user_name)} ({safe_escape(user_role)})")
        else:
            col_sc1, col_sc2 = st.columns([1.5, 3])
            with col_sc1:
                st.markdown("<strong style='font-size: 0.88rem; color: var(--mt-text); line-height: 2.2;'>Filter View Scope:</strong>", unsafe_allow_html=True)
            with col_sc2:
                scope = st.radio("Task View Scope", ["My Personal Commitments", f"Organization-wide All Commitments ({user_role} View)"], horizontal=True, label_visibility="collapsed")
            
            if "Personal" in scope:
                tasks = repository.get_action_items(db, user_id=current_user_id, org_id=org_id)
                user_name = current_user.full_name or current_user.username if current_user else "You"
                st.caption(f"Showing personal commitments assigned to {safe_escape(user_name)}")
            else:
                tasks = repository.get_action_items(db, org_id=org_id)
                st.caption(f"Showing all organizational task commitments across Acme Global ({safe_escape(user_role)} view)")

        # Metrics
        total = len(tasks)
        in_progress = sum(1 for t in tasks if t.status in ["In Progress", "Approved", "Scheduled"])
        completed = sum(1 for t in tasks if t.status == "Completed")
        blocked = sum(1 for t in tasks if t.status == "Blocked")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Total Tasks", str(total), "list-check", "Assigned in scope")
        with c2:
            metric_card("Active / In Progress", str(in_progress), "zap", "Currently underway")
        with c3:
            metric_card("Blocked / Risk", str(blocked), "alert-triangle", "Needs resolution")
        with c4:
            metric_card("Completed", str(completed), "check-circle", "Finished deliverables")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        
        tabs = st.tabs(["Active Tasks", "Blocked & Overdue", "Completed Deliverables", "Audit Trail"])
        
        with tabs[0]:
            active = [t for t in tasks if t.status not in ["Completed", "Blocked", "Rejected"]]
            if not active:
                empty_state("check-circle", "No active pending tasks", "You're all caught up with active commitments in this view!")
            else:
                for item in active:
                    render_task_card(item, db, current_user_id, user_role, is_blocked=False, show_meeting=True)

        with tabs[1]:
            blocked_tasks = [t for t in tasks if t.status in ["Blocked", "Overdue"] or t.priority == "Urgent"]
            if not blocked_tasks:
                empty_state("check-circle", "No blocked tasks", "No active dependencies or overdue commitments flagged.")
            else:
                for item in blocked_tasks:
                    render_task_card(item, db, current_user_id, user_role, is_blocked=True, show_meeting=True)

        with tabs[2]:
            comp_tasks = [t for t in tasks if t.status == "Completed"]
            if not comp_tasks:
                empty_state("folder", "No completed tasks yet", "Complete tasks to build your deliverable track record.")
            else:
                for item in comp_tasks:
                    render_task_card(item, db, current_user_id, user_role, is_blocked=False, show_meeting=True)

        with tabs[3]:
            st.markdown("<h4 style='color: var(--mt-text); margin-top: 0; font-weight: 700; font-size: 1.05rem;'>Compliance & Task Audit Trail</h4>", unsafe_allow_html=True)
            events = repository.get_audit_trail(db, org_id=org_id, entity_type="task", limit=30)
            if not events:
                empty_state("shield-check", "No task audit events recorded yet", "Action item state transitions and approvals will appear here.")
            else:
                with st.container(border=True):
                    for i, ev in enumerate(events):
                        if i > 0:
                            st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 8px 0;'></div>", unsafe_allow_html=True)
                        ts = ev.timestamp.strftime("%Y-%m-%d %H:%M:%S") if ev.timestamp else "Recently"
                        col_ev1, col_ev2 = st.columns([3.5, 1.2])
                        with col_ev1:
                            st.markdown(f"<strong style='color: var(--mt-text); font-size: 0.88rem;'>[{safe_escape(ev.action)}]</strong> Task #{safe_escape(str(ev.entity_id))}", unsafe_allow_html=True)
                            if ev.details:
                                st.markdown(f"<span style='color: var(--mt-text-secondary); font-size: 0.84rem;'>{safe_escape(ev.details)}</span>", unsafe_allow_html=True)
                            if ev.transcript_excerpt:
                                st.markdown(f"<div style='font-style: italic; font-size: 0.82rem; color: var(--mt-text-secondary); margin-top: 2px;'>Source excerpt: \"{safe_escape(ev.transcript_excerpt)}\"</div>", unsafe_allow_html=True)
                        with col_ev2:
                            st.markdown(f"<div style='text-align: right; color: var(--mt-text-secondary); font-size: 0.78rem;'>{ts}<br>by <strong>{safe_escape(ev.actor_username)}</strong></div>", unsafe_allow_html=True)
    finally:
        db.close()

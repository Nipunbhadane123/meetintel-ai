import streamlit as st
from storage.database import SessionLocal
from storage.models import User, ActionItem, Organization
from storage import repository
from ui.components import page_header, empty_state, render_status_badge, render_metric_card, safe_escape, get_icon_svg

def render_team_page():
    page_header(
        title="Team & Organization Directory",
        subtitle="Manage organization members, departments, role permissions, and individual commitment accountability.",
        category="Organization & Governance",
        badge_text="Role-Based Access",
        badge_type="accent",
        icon="users"
    )
    
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        user_role = current_user.role if current_user else "Employee"
        org_id = current_user.org_id if current_user else "org-default-001"

        # Backend Authorization Check
        if user_role not in ["Admin", "Team Lead"]:
            st.error("🛡️ Access Restricted: You must be a Team Lead or Organization Administrator to access the Team Directory.")
            return

        org = db.query(Organization).filter(Organization.id == org_id).first()
        org_name = org.name if org else "Acme Global Technologies"

        users = repository.get_all_org_users(db, org_id=org_id)
        all_tasks = repository.get_action_items(db, org_id=org_id)

        total_members = len(users)
        admins = sum(1 for u in users if u.role == "Admin")
        leads = sum(1 for u in users if u.role == "Team Lead")
        engineers = sum(1 for u in users if u.role == "Employee")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            render_metric_card("Total Members", str(total_members), org_name, "users")
        with c2:
            render_metric_card("Administrators", str(admins), "Governance access", "shield-check")
        with c3:
            render_metric_card("Team Leads", str(leads), "Approval authority", "badge-check")
        with c4:
            render_metric_card("Contributors", str(engineers), "Execution ownership", "list-check")

        st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 12px 0; font-weight: 700; font-size: 1.05rem;'>Member Roster & Accountability</h4>", unsafe_allow_html=True)

        for u in users:
            u_tasks = [t for t in all_tasks if t.assigned_user_id == u.id or t.assigned_to in [u.full_name, u.username]]
            active_cnt = sum(1 for t in u_tasks if t.status in ["In Progress", "Approved", "Scheduled", "Pending"])
            comp_cnt = sum(1 for t in u_tasks if t.status == "Completed")
            blocked_cnt = sum(1 for t in u_tasks if t.status == "Blocked")

            with st.container(border=True):
                col_u1, col_u2, col_u3 = st.columns([2.5, 2, 1.5])
                with col_u1:
                    initial = (u.full_name or u.username or "U")[0].upper()
                    st.markdown(
                        f"<div style='display: flex; align-items: center; gap: 10px;'>"
                        f"<div style='width: 32px; height: 32px; border-radius: 50%; background: var(--mt-primary-light); color: var(--mt-primary); font-weight: 700; display: flex; align-items: center; justify-content: center; font-size: 0.85rem;'>{safe_escape(initial)}</div>"
                        f"<div>"
                        f"<strong style='font-size: 1rem; color: var(--mt-text);'>{safe_escape(u.full_name or u.username)}</strong>"
                        f"<div style='font-size: 0.78rem; color: var(--mt-text-secondary);'>{safe_escape(u.email or 'No email')} &bull; {safe_escape(u.department or 'Engineering')}</div>"
                        f"</div>"
                        f"</div>",
                        unsafe_allow_html=True
                    )
                with col_u2:
                    st.markdown(f"<span>Role: {render_status_badge(u.role, 'status')}</span>", unsafe_allow_html=True)
                    st.caption(f"Timezone: {safe_escape(u.timezone or 'UTC')}")
                with col_u3:
                    st.markdown(f"<div style='text-align: right;'><span style='color: var(--mt-primary); font-weight: 600;'>{active_cnt} Active</span> • <span style='color: var(--mt-success); font-weight: 600;'>{comp_cnt} Done</span></div>", unsafe_allow_html=True)
                    if blocked_cnt > 0:
                        st.markdown(f"<div style='text-align: right; color: var(--mt-error); font-size: 0.8rem; font-weight: 600; margin-top: 2px;'>⚠️ {blocked_cnt} Blocked</div>", unsafe_allow_html=True)
    finally:
        db.close()

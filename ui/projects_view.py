import streamlit as st
import datetime
import logging
from sqlalchemy.exc import IntegrityError

from storage.database import get_db
from storage.models import Project, ActionItem
from storage import repository
from ui.components import page_header, empty_state, render_status_badge, safe_escape, metric_card, get_icon_svg

logger = logging.getLogger(__name__)

def render_projects_page():
    page_header(
        "Projects & Strategic Milestones",
        "Group meeting outcomes, track cross-functional initiatives, and monitor deliverable completion velocity.",
        category="Planning & Intelligence",
        badge_text="Strategic Execution",
        badge_type="accent",
        icon="target"
    )
    
    db = next(get_db())
    current_user_id = st.session_state.get('user_id')
    current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
    user_role = current_user.role if current_user else "Employee"
    org_id = current_user.org_id if current_user else "org-default-001"

    projects = repository.get_projects(db, org_id=org_id)
    all_org_tasks = db.query(ActionItem).filter(ActionItem.org_id == org_id).all()
    
    total_projects = len(projects)
    total_completed = sum(1 for t in all_org_tasks if t.status == "Completed")
    total_open = sum(1 for t in all_org_tasks if t.status not in ["Completed", "Rejected"])
    total_blocked = sum(1 for t in all_org_tasks if t.status == "Blocked")

    # 4 Subtle Summary Metrics Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Active Initiatives", str(total_projects), "target", "Strategic tracks")
    with c2:
        metric_card("Delivered Outcomes", str(total_completed), "check-circle", "Finished deliverables")
    with c3:
        metric_card("Open Deliverables", str(total_open), "list-check", "Across all projects")
    with c4:
        metric_card("At-Risk Items", str(total_blocked), "alert-triangle", "Active dependencies")

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Leadership Project Creation Form
    if user_role in ["Admin", "Team Lead"]:
        with st.expander("＋ Register Strategic Project", expanded=False):
            with st.form("create_project_form"):
                c_p1, c_p2 = st.columns([2.5, 1.5])
                with c_p1:
                    p_name = st.text_input("Project Name *", placeholder="e.g. Enterprise Security Architecture")
                    p_desc = st.text_area("Scope & Objectives", placeholder="Key objectives, milestones, and deliverable commitments...")
                with c_p2:
                    p_status = st.selectbox("Status", ["Active", "At Risk", "Completed", "On Hold"])
                    p_date = st.date_input("Target Delivery Date", value=datetime.date.today() + datetime.timedelta(days=45))
                
                submitted = st.form_submit_button("Save Strategic Initiative", type="primary")
                if submitted:
                    if not p_name or not p_name.strip():
                        st.warning("Please provide a valid project name.")
                    else:
                        target_dt = datetime.datetime.combine(p_date, datetime.time.min)
                        try:
                            repository.create_project(
                                db,
                                org_id=org_id,
                                name=p_name.strip(),
                                description=p_desc.strip() if p_desc else None,
                                status=p_status,
                                target_date=target_dt
                            )
                            st.toast(f"Project '{p_name.strip()}' registered successfully!")
                            st.rerun()
                        except IntegrityError as ie:
                            logger.error(f"Database constraint error creating project: {getattr(ie, 'orig', ie)}")
                            st.error("Database constraint notice: Project name must be unique within organization.")
                        except Exception as ex:
                            logger.error(f"Unexpected error creating project: {ex}", exc_info=True)
                            st.error(f"Failed to create project: {ex}")

    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

    if not projects:
        empty_state(
            "target",
            "No Strategic Projects Registered",
            "Track cross-functional initiatives and deliverables by initializing standard strategic milestones or creating a custom project above."
        )
        if user_role in ["Admin", "Team Lead"]:
            col_seed1, _ = st.columns([1.8, 3])
            with col_seed1:
                if st.button("✦ Initialize Standard Strategic Initiatives", type="primary", use_container_width=True):
                    try:
                        repository.seed_default_projects(db, org_id=org_id)
                        st.toast("Standard organizational projects initialized!")
                        st.rerun()
                    except IntegrityError as ie:
                        logger.error(f"IntegrityError initializing default projects: {getattr(ie, 'orig', ie)}")
                        st.error("Database constraint notice during initialization. Operation safe-rolled back.")
                    except Exception as ex:
                        logger.error(f"Failed to seed default projects: {ex}", exc_info=True)
                        st.error(f"Initialization failed: {ex}")
        return

    # Render Project Rows (Cleaner List-Based Presentation)
    for p in projects:
        specific_tasks = db.query(ActionItem).filter(
            ActionItem.org_id == org_id,
            ActionItem.project_id == p.id
        ).all()
        
        if not specific_tasks:
            specific_tasks = db.query(ActionItem).filter(ActionItem.org_id == org_id).all()
            
        completed_count = sum(1 for t in specific_tasks if t.status == "Completed")
        blocked_count = sum(1 for t in specific_tasks if t.status == "Blocked")
        total_p_tasks = len(specific_tasks)
        progress_pct = int((completed_count / total_p_tasks * 100)) if total_p_tasks > 0 else 0

        target_date_str = p.target_date.strftime('%B %d, %Y') if p.target_date else 'Target Date TBD'

        with st.container(border=True):
            col_ph1, col_ph2 = st.columns([3.8, 1.4])
            with col_ph1:
                st.markdown(
                    f"<div style='display: flex; align-items: center; gap: 6px; margin-bottom: 4px;'>"
                    f"<span style='color: var(--mt-primary); font-size: 0.72rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase;'>Strategic Initiative</span>"
                    f"<span style='color: var(--mt-border);'>•</span>"
                    f"<span style='color: var(--mt-text-secondary); font-size: 0.72rem; font-weight: 500;'>Target: {target_date_str.upper()}</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.markdown(f"<h3 style='margin: 0 0 6px 0; font-size: 1.2rem; font-weight: 700; color: var(--mt-text); letter-spacing: -0.015em;'>{safe_escape(p.name)}</h3>", unsafe_allow_html=True)
                if p.description:
                    st.markdown(f"<p style='color: var(--mt-text-secondary); font-size: 0.88rem; line-height: 1.5; margin: 0 0 10px 0;'>{safe_escape(p.description)}</p>", unsafe_allow_html=True)
            with col_ph2:
                st.markdown(f"<div style='text-align: right;'>{render_status_badge(p.status, 'status')}</div>", unsafe_allow_html=True)

            # Progress Bar & Deliverables Metrics
            st.markdown(
                f"<div style='display: flex; justify-content: space-between; align-items: center; font-size: 0.78rem; margin-bottom: 4px;'>"
                f"<span style='color: var(--mt-text-secondary); font-weight: 600; text-transform: uppercase;'>Deliverable Completion Velocity</span>"
                f"<strong style='color: var(--mt-primary); font-size: 0.88rem;'>{progress_pct}%</strong>"
                f"</div>",
                unsafe_allow_html=True
            )
            st.progress(progress_pct / 100.0)

            col_pt1, col_pt2, col_pt3 = st.columns([1.5, 1.5, 2])
            with col_pt1:
                st.markdown(f"<span style='font-size: 0.82rem; color: var(--mt-text-secondary);'>Open Tasks: <strong>{total_p_tasks - completed_count}</strong></span>", unsafe_allow_html=True)
            with col_pt2:
                st.markdown(f"<span style='font-size: 0.82rem; color: var(--mt-text-secondary);'>Completed: <strong style='color: var(--mt-success);'>{completed_count}</strong></span>", unsafe_allow_html=True)
            with col_pt3:
                blocked_html = f"<span style='color: var(--mt-error); font-weight: 600;'>⚠️ {blocked_count} Blocked</span>" if blocked_count > 0 else "<span style='color: var(--mt-success); font-weight: 600;'>✓ Zero Blockers</span>"
                st.markdown(f"<div style='text-align: right; font-size: 0.82rem;'>{blocked_html}</div>", unsafe_allow_html=True)

            # Deliverables Expander with subtle light dividers
            with st.expander(f"📋 Associated Deliverables ({len(specific_tasks)})", expanded=False):
                if not specific_tasks:
                    st.caption("No action items currently linked to this initiative.")
                else:
                    for idx, t in enumerate(specific_tasks[:6]):
                        if idx > 0:
                            st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 6px 0;'></div>", unsafe_allow_html=True)
                        col_t1, col_t2 = st.columns([3.5, 1.2])
                        with col_t1:
                            st.markdown(f"<strong style='color: var(--mt-text); font-size: 0.88rem;'>{safe_escape(t.task)}</strong> <span style='color: var(--mt-text-secondary); font-size: 0.8rem;'>({safe_escape(t.assigned_to, default='Unassigned')})</span>", unsafe_allow_html=True)
                        with col_t2:
                            st.markdown(f"<div style='text-align: right;'>{render_status_badge(t.status, 'status')}</div>", unsafe_allow_html=True)

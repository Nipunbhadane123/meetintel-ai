import streamlit as st
import datetime
import pandas as pd
from storage.database import SessionLocal
from storage.models import AuditEvent, User
from storage import repository
from ui.components import page_header, empty_state, render_status_badge, safe_escape, get_icon_svg

def render_audit_page():
    page_header(
        title="Compliance & System Audit Trail",
        subtitle="Immutable, non-repudiable audit log of task approvals, status modifications, decision revisions, and integrations.",
        category="Administration & Governance",
        badge_text="Compliance Verified",
        badge_type="accent",
        icon="shield-check"
    )
    
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        user_role = current_user.role if current_user else "Employee"
        org_id = current_user.org_id if current_user else "org-default-001"

        # Backend Authorization Check
        if user_role not in ["Admin", "Team Lead"]:
            st.error("🛡️ Access Restricted: You must be a Team Lead or Organization Administrator to view the compliance audit trail.")
            return

        # Unboxed Filter Controls
        col_f1, col_f2 = st.columns([2, 1])
        with col_f1:
            entity_filter = st.selectbox("Filter by Entity Type", ["All Entities", "task", "decision", "meeting", "calendar", "notification"], label_visibility="collapsed")
        with col_f2:
            action_filter = st.selectbox("Filter by Action Type", ["All Actions", "APPROVE", "REJECT", "UPDATE", "REASSIGN", "SYNC", "CREATE"], label_visibility="collapsed")

        events = repository.get_audit_trail(
            db,
            org_id=org_id,
            entity_type=None if entity_filter == "All Entities" else entity_filter,
            limit=50
        )

        if action_filter != "All Actions":
            events = [e for e in events if e.action == action_filter]

        st.markdown(
            f"<div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0 14px 0;'>"
            f"<span style='color: var(--mt-text-secondary); font-size: 0.84rem; font-weight: 500;'>Displaying <strong>{len(events)}</strong> recorded audit events for Acme Global</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        if not events:
            empty_state("shield-check", "No audit events found", "No compliance events match your current filter selection.")
            return

        with st.container(border=True):
            for i, ev in enumerate(events):
                if i > 0:
                    st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 8px 0;'></div>", unsafe_allow_html=True)
                ts = ev.timestamp.strftime("%Y-%m-%d %H:%M:%S") if ev.timestamp else "Recently"
                col_e1, col_e2 = st.columns([3.5, 1.2])
                with col_e1:
                    st.markdown(f"<strong style='color: var(--mt-text); font-size: 0.92rem;'>[{safe_escape(ev.action)}]</strong> <span style='font-weight: 600; color: var(--mt-primary); font-size: 0.88rem;'>{safe_escape(ev.entity_type.upper())} #{safe_escape(str(ev.entity_id))}</span>", unsafe_allow_html=True)
                    if ev.details:
                        st.markdown(f"<div style='color: var(--mt-text-secondary); font-size: 0.86rem; margin-top: 2px;'>{safe_escape(ev.details)}</div>", unsafe_allow_html=True)
                    if ev.transcript_excerpt:
                        st.markdown(f"<div style='font-style: italic; font-size: 0.82rem; color: var(--mt-text-secondary); margin-top: 3px;'>Verbatim Context: \"{safe_escape(ev.transcript_excerpt)}\"</div>", unsafe_allow_html=True)
                with col_e2:
                    st.markdown(f"<div style='text-align: right; color: var(--mt-text-secondary); font-size: 0.78rem;'>{ts}<br>Actor: <strong style='color: var(--mt-text);'>{safe_escape(ev.actor_username)}</strong></div>", unsafe_allow_html=True)

        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        csv = pd.DataFrame([{
            "Timestamp": e.timestamp,
            "Actor": e.actor_username,
            "Action": e.action,
            "Entity Type": e.entity_type,
            "Entity ID": e.entity_id,
            "Details": e.details,
            "Transcript Excerpt": e.transcript_excerpt
        } for e in events]).to_csv(index=False)
        st.download_button("↓ Export Audit Trail (CSV)", data=csv, file_name="Compliance_Audit_Trail.csv", mime="text/csv", type="secondary")
    finally:
        db.close()

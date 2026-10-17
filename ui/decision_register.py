import streamlit as st
import pandas as pd
from storage.database import SessionLocal
from storage.models import Decision, Meeting
from storage import repository
from ui.components import page_header, empty_state, render_decision_card, safe_escape, get_icon_svg

def render_decision_register_page():
    db = SessionLocal()
    try:
        current_user_id = st.session_state.get('user_id')
        current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
        user_role = current_user.role if current_user else "Employee"
        org_id = current_user.org_id if current_user else "org-default-001"
        
        page_header(
            "Organizational Decision Register",
            "Traceable repository of strategic agreements, rationale, alternatives, and revision history.",
            category="Governance & Truth",
            badge_text="Immutable Register",
            badge_type="accent",
            icon="scale"
        )

        # Unboxed Filter & Search Controls Bar
        col_s1, col_s2 = st.columns([3.2, 1.2])
        with col_s1:
            search_query = st.text_input(
                "Search Decisions",
                placeholder="Filter by decision topic, agreement, rationale, or context...",
                label_visibility="collapsed"
            )
        with col_s2:
            status_filter = st.selectbox(
                "Status Filter",
                ["All Statuses", "Approved", "Proposed", "Superseded", "Rejected"],
                label_visibility="collapsed"
            )

        decisions = repository.get_decisions(
            db,
            org_id=org_id,
            status=None if status_filter == "All Statuses" else status_filter
        )
        
        if search_query:
            q = search_query.lower()
            decisions = [
                d for d in decisions
                if q in (d.decision or '').lower() or q in (d.context or '').lower() or q in (d.title or '').lower() or q in (d.rationale or '').lower()
            ]

        st.markdown(
            f"<div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0 14px 0;'>"
            f"<span style='color: var(--mt-text-secondary); font-size: 0.84rem; font-weight: 500;'>Showing <strong>{len(decisions)}</strong> verified decision records</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        if not decisions:
            empty_state(
                "scale",
                "No Decisions Match Your Criteria",
                "Try adjusting your keyword query or status filter to see verified organizational agreements."
            )
            return

        for d in decisions:
            render_decision_card(d, db, current_user_id, user_role)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        
        # Clean Unboxed Export Section
        col_exp1, col_exp2 = st.columns([3.2, 1.3])
        with col_exp1:
            st.markdown("<strong style='color: var(--mt-text); font-size: 0.92rem;'>Export Immutable Decision Log</strong>", unsafe_allow_html=True)
            st.caption("Download the complete immutable decision register including verbatim evidence, rationale, and proposer metadata.")
        with col_exp2:
            csv = pd.DataFrame([{
                "ID": d.id,
                "Title": d.title,
                "Decision": d.decision,
                "Rationale": d.rationale,
                "Alternatives": d.alternatives,
                "Evidence Excerpt": d.evidence_excerpt,
                "Status": d.status,
                "Proposer": d.proposer,
                "Meeting ID": d.meeting_id
            } for d in decisions]).to_csv(index=False)
            st.download_button(
                "↓ Export Register (CSV)",
                data=csv,
                file_name="Decision_Register.csv",
                mime="text/csv",
                type="secondary",
                use_container_width=True
            )
    finally:
        db.close()

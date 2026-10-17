import streamlit as st
import datetime
from storage.database import SessionLocal
from storage.repository import get_all_meetings
from ui.components import render_meeting_card, empty_state, page_header, safe_escape, get_icon_svg

def render_meetings_list():
    db = SessionLocal()
    try:
        user_id = st.session_state.get('user_id')
        
        try:
            all_meetings = get_all_meetings(db, user_id=user_id)
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Meeting List DB Error: {e}")
            st.error("Unable to load meeting library. Database connection is temporarily busy.")
            if st.button("Retry Connection", type="primary"):
                st.rerun()
            return

        # Header with Quick Action
        col_h1, col_h2 = st.columns([3.8, 1.3])
        with col_h1:
            page_header(
                "Meeting Intelligence Library",
                "Browse, filter, and inspect AI-generated executive dossiers, verified action items, and transcripts.",
                category="Intelligence Repository",
                badge_text=f"{len(all_meetings)} Sessions",
                badge_type="accent",
                icon="mic"
            )
        with col_h2:
            st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
            if st.button("＋ Process Meeting", key="btn_lib_new_meeting", type="primary", use_container_width=True):
                st.session_state['current_page'] = "New Meeting"
                st.rerun()

        if not all_meetings:
            empty_state(
                "mic",
                "No Recorded Sessions Yet",
                "Upload an audio file or connect a meeting service to produce automated meeting intelligence.",
                action_label="Upload Meeting Recording",
                action_key="lib_empty_upload"
            )
            if st.session_state.get("lib_empty_upload"):
                st.session_state['current_page'] = "New Meeting"
                st.rerun()
            return

        # Unboxed Filter & Search Controls Bar
        col_s1, col_s2, col_s3 = st.columns([2.5, 1.2, 1.3])
        with col_s1:
            search_query = st.text_input(
                "Search Library",
                placeholder="Search by meeting title, topic, or summary excerpt...",
                label_visibility="collapsed"
            )
        with col_s2:
            status_filter = st.selectbox(
                "Status Filter",
                ["All Statuses", "Completed", "Processing", "Pending", "Failed"],
                label_visibility="collapsed"
            )
        with col_s3:
            sort_by = st.selectbox(
                "Sort By",
                ["Newest Date", "Oldest Date", "Duration (Longest)", "Title (A-Z)"],
                label_visibility="collapsed"
            )

        # Filter Logic
        filtered = list(all_meetings)
        if search_query:
            q = search_query.lower()
            filtered = [
                m for m in filtered
                if q in (m.title or '').lower() or q in (m.executive_summary or '').lower()
            ]

        if status_filter != "All Statuses":
            filtered = [
                m for m in filtered
                if status_filter.lower() in (m.processing_status or '').lower()
            ]

        # Sort Logic
        if sort_by == "Newest Date":
            filtered.sort(key=lambda m: m.date or datetime.datetime.min, reverse=True)
        elif sort_by == "Oldest Date":
            filtered.sort(key=lambda m: m.date or datetime.datetime.min, reverse=False)
        elif sort_by == "Duration (Longest)":
            filtered.sort(key=lambda m: m.duration or 0.0, reverse=True)
        elif sort_by == "Title (A-Z)":
            filtered.sort(key=lambda m: (m.title or '').lower(), reverse=False)

        # Results Status Label
        st.markdown(
            f"<div style='display: flex; justify-content: space-between; align-items: center; margin: 8px 0 14px 0;'>"
            f"<span style='color: var(--mt-text-secondary); font-size: 0.84rem; font-weight: 500;'>Showing <strong>{len(filtered)}</strong> of {len(all_meetings)} recorded sessions</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        if not filtered:
            empty_state(
                "search",
                "No Matching Meetings Found",
                "No sessions matched your search filters. Try broadening your keyword or status criteria."
            )
        else:
            for m in filtered:
                render_meeting_card(m, button_key=f"lib_card_{m.id}")
    finally:
        db.close()

import streamlit as st
from storage.database import get_db, SessionLocal
from storage.repository import get_all_meetings
from storage.models import TranscriptSegment
from ui.components import empty_state, transcript_message, page_header, render_status_badge, safe_escape, get_icon_svg

def render_transcripts_list():
    page_header(
        title="Transcript Library",
        subtitle="Search, inspect, and extract dialogue segments across all recorded organizational sessions.",
        category="Intelligence Repository",
        badge_text="Verbatim Logs",
        badge_type="accent",
        icon="file-text"
    )
    
    db = SessionLocal()
    user_id = st.session_state.get('user_id')
    
    try:
        meetings = get_all_meetings(db, user_id=user_id)
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Transcripts DB Error: {e}")
        st.error("Unable to load transcripts right now. Please try again.")
        if st.button("Retry"):
            st.rerun()
        db.close()
        return
    
    if not meetings:
        empty_state("file-text", "No transcripts found", "Upload a meeting to generate transcripts.")
        db.close()
        return
        
    search_query = st.text_input("Search transcripts by meeting name or keywords...", label_visibility="collapsed", placeholder="Search transcripts by meeting name or keywords...")
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    for meeting in meetings:
        segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting.id).order_by(TranscriptSegment.start).all()
        if not segments:
            continue
            
        if search_query:
            match_found = any(search_query.lower() in s.text.lower() for s in segments) or (search_query.lower() in (meeting.title or '').lower())
            if not match_found:
                continue
                
        preview_text = segments[0].text if segments else "No transcript available."
        with st.container(border=True):
            col_icon, col_content, col_actions = st.columns([0.5, 7.5, 2.5])
            
            with col_icon:
                file_icon = get_icon_svg("file-text", size=22, color="#6C4DFF")
                st.markdown(f"<div style='line-height: 1; margin-top: 0.25rem;'>{file_icon}</div>", unsafe_allow_html=True)
                
            with col_content:
                st.markdown(f"<h3 style='margin: 0 0 4px 0; font-size: 1.15rem; color: var(--mt-text); font-weight: 700;'>{safe_escape(meeting.title)}</h3>", unsafe_allow_html=True)
                duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s" if meeting.duration else "N/A"
                date_str = meeting.date.strftime('%B %d, %Y') if meeting.date else "Recent"
                st.markdown(f"<div style='color: var(--mt-text-secondary); font-size: 0.84rem; margin-bottom: 6px;'>{date_str} • {duration_str} • {meeting.speaker_count or 0} speakers</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: var(--mt-text-secondary); font-size: 0.88rem; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;'>{safe_escape(preview_text)}</div>", unsafe_allow_html=True)
                
            with col_actions:
                st.markdown(f"<div style='text-align: right; margin-bottom: 10px;'>{render_status_badge(meeting.processing_status, 'status')}</div>", unsafe_allow_html=True)
                
                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if st.button("Snippets", key=f"btn_snip_{meeting.id}", type="secondary", use_container_width=True):
                        st.session_state[f'show_snip_{meeting.id}'] = not st.session_state.get(f'show_snip_{meeting.id}', False)
                        st.rerun()
                with col_btn2:
                    if st.button("View", key=f"btn_res_{meeting.id}", type="primary", use_container_width=True):
                        st.session_state['current_meeting_id'] = meeting.id
                        st.session_state['current_page'] = "Meeting Results"
                        st.rerun()
                        
            if st.session_state.get(f'show_snip_{meeting.id}', False):
                st.markdown("<hr style='border: 0; border-top: 1px solid var(--mt-border); margin: 12px 0;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='color: var(--mt-text); font-size: 0.95rem; font-weight: 700; margin-bottom: 8px;'>Dialogue Snippets (First 3 Turns)</h4>", unsafe_allow_html=True)
                for seg in segments[:3]:
                    m, s = divmod(int(seg.start), 60)
                    ts = f"{m:02d}:{s:02d}"
                    transcript_message(seg.speaker, ts, seg.text)
    db.close()

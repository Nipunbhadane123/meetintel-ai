import streamlit as st
from storage.database import get_db, SessionLocal
from storage.repository import get_all_meetings
from storage.models import TranscriptSegment
from ui.components import empty_state, transcript_message

def render_transcripts_list():
    st.markdown("""
        <div class="page-title-container" style="margin-bottom: var(--mt-space-xl);">
            <h2 class="page-title" style="color: var(--mt-text); font-weight: 750; font-size: 2.2rem; margin: 0 0 8px 0; letter-spacing: -0.02em;"><span style="color: var(--mt-primary);">☶</span> Transcript Library</h2>
            <p class="page-subtitle" style="color: var(--mt-text-secondary); font-size: 1.1rem; margin: 0;">Search and view all meeting transcripts.</p>
        </div>
    """, unsafe_allow_html=True)
    
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
        empty_state("📭", "No transcripts found", "Upload a meeting to generate transcripts.")
        db.close()
        return
        
    search_query = st.text_input("🔍 Search transcripts by meeting name or keywords...", label_visibility="collapsed", placeholder="🔍 Search transcripts by meeting name or keywords...")
    st.markdown("<div style='height: var(--mt-space-lg);'></div>", unsafe_allow_html=True)
    
    for meeting in meetings:
        # Check if meeting has segments
        segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting.id).order_by(TranscriptSegment.start).all()
        if not segments:
            continue
            
        # If searching, filter meetings that match
        if search_query:
            match_found = any(search_query.lower() in s.text.lower() for s in segments) or (search_query.lower() in meeting.title.lower())
            if not match_found:
                continue
                
        preview_text = segments[0].text if segments else "No transcript available."
        with st.container():
            st.markdown(f"""
                <div class="transcript-card-marker-{meeting.id}"></div>
                <style>
                div[data-testid="stVerticalBlock"]:has(.transcript-card-marker-{meeting.id}):not(:has(div[data-testid="stVerticalBlock"]:has(.transcript-card-marker-{meeting.id}))) {{
                    background: var(--mt-surface) !important;
                    border-radius: var(--mt-radius-xl) !important;
                    padding: var(--mt-space-xl) !important;
                    box-shadow: var(--mt-shadow-soft) !important;
                    border: 1px solid var(--mt-border) !important;
                    margin-bottom: var(--mt-space-lg) !important;
                    transition: var(--mt-transition) !important;
                }}
                div[data-testid="stVerticalBlock"]:has(.transcript-card-marker-{meeting.id}):not(:has(div[data-testid="stVerticalBlock"]:has(.transcript-card-marker-{meeting.id}))):hover {{
                    box-shadow: var(--mt-shadow-hover) !important;
                    border-color: rgba(109, 61, 245, 0.3) !important;
                    transform: translateY(-2px) !important;
                }}
                .transcript-card-marker-{meeting.id} {{ display: none; }}
                </style>
            """, unsafe_allow_html=True)
            
            col_icon, col_content, col_actions = st.columns([0.5, 8, 2.5])
            
            with col_icon:
                st.markdown("<div style='font-size: 1.5rem; line-height: 1; margin-top: 0.25rem; color: var(--mt-primary);'>☶</div>", unsafe_allow_html=True)
                
            with col_content:
                st.markdown(f"<h3 style='margin: 0 0 6px 0; font-size: 1.15rem; color: var(--mt-text); font-weight: 650;'>{meeting.title}</h3>", unsafe_allow_html=True)
                duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s"
                st.markdown(f"<div style='color: var(--mt-text-secondary); font-size: 0.85rem; margin-bottom: 8px;'>{meeting.date.strftime('%Y-%m-%d')} • {duration_str} • {meeting.speaker_count} speakers</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: var(--mt-text-muted); font-size: 0.9rem; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;'>{preview_text}</div>", unsafe_allow_html=True)
                
            with col_actions:
                # Status Badge
                status_lower = meeting.processing_status.lower()
                badge_class = "badge-completed" if "complete" in status_lower else "badge-processing" if "process" in status_lower else "badge-pending"
                badge_icon = "✓" if "complete" in status_lower else "●"
                
                st.markdown(f"<div style='text-align: right; margin-bottom: var(--mt-space-md);'><span class='badge {badge_class}'>{badge_icon} {meeting.processing_status}</span></div>", unsafe_allow_html=True)
                
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
            st.markdown("<div style='margin-top: -1.5rem; margin-bottom: 1.5rem; padding: 1.5rem; background: var(--mt-surface-soft); border-radius: 0 0 var(--mt-radius-xl) var(--mt-radius-xl); border: 1px solid var(--mt-border); border-top: none;'>", unsafe_allow_html=True)
            for seg in segments[:5]: # show up to 5
                if search_query and search_query.lower() not in seg.text.lower():
                    continue
                m, s = divmod(int(seg.start), 60)
                h, m = divmod(m, 60)
                ts = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
                text = seg.text.replace(search_query, f"<b>{search_query}</b>") if search_query else seg.text
                transcript_message(seg.speaker, ts, text)
            if len(segments) > 5 and not search_query:
                st.markdown("<div style='text-align: center; color: var(--mt-text-muted); font-size: 0.85rem;'>+ more segments... (Click View)</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
    db.close()

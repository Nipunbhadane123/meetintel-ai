import streamlit as st
from storage.database import get_db
from storage.repository import get_all_meetings
from storage.models import TranscriptSegment
from ui.components import section_header, empty_state, transcript_message

def render_transcripts_list():
    section_header("📄 Transcript Library", "Search and view all meeting transcripts")
    
    db = next(get_db())
    meetings = get_all_meetings(db)
    
    if not meetings:
        empty_state("📭", "No transcripts found", "Upload a meeting to generate transcripts.")
        return
        
    st.write("") # small spacing
    search_query = st.text_input("🔍 Search transcripts by meeting name or keywords...", label_visibility="collapsed", placeholder="🔍 Search transcripts by meeting name or keywords...")
    st.write("") # small spacing
    
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
                    background: var(--surface) !important;
                    border-radius: 20px !important;
                    padding: 1.5rem !important;
                    box-shadow: var(--shadow-soft) !important;
                    border: 1px solid #E2E8F0 !important;
                    margin-bottom: 1rem !important;
                    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
                }}
                div[data-testid="stVerticalBlock"]:has(.transcript-card-marker-{meeting.id}):not(:has(div[data-testid="stVerticalBlock"]:has(.transcript-card-marker-{meeting.id}))):hover {{
                    box-shadow: var(--shadow-hover) !important;
                    transform: translateY(-1px) !important;
                }}
                .transcript-card-marker-{meeting.id} {{ display: none; }}
                </style>
            """, unsafe_allow_html=True)
            
            col_icon, col_content, col_actions = st.columns([1, 8, 3])
            
            with col_icon:
                st.markdown("<div style='font-size: 2.5rem; line-height: 1; margin-top: 0.25rem;'>📄</div>", unsafe_allow_html=True)
                
            with col_content:
                st.markdown(f"<h3 style='margin: 0 0 0.25rem 0; font-size: 1.15rem; color: var(--text-main); font-weight: 600;'>{meeting.title}</h3>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0.5rem;'>{meeting.date.strftime('%Y-%m-%d')} • {meeting.duration}s • {meeting.speaker_count} speakers</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: var(--text-muted); font-size: 0.9rem; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;'>{preview_text}</div>", unsafe_allow_html=True)
                
            with col_actions:
                # Status Badge
                status_lower = meeting.processing_status.lower()
                badge_class = "badge-completed" if "complete" in status_lower else "badge-processing" if "process" in status_lower else "badge-pending"
                badge_icon = "✓" if "complete" in status_lower else "●"
                
                st.markdown(f"<div style='text-align: right; margin-bottom: 0.75rem;'><span class='badge {badge_class}'>{badge_icon} {meeting.processing_status}</span></div>", unsafe_allow_html=True)
                
                if st.button("View Meeting →", key=f"btn_res_{meeting.id}", type="primary", use_container_width=True):
                    st.session_state['current_meeting_id'] = meeting.id
                    st.session_state['current_page'] = "Meeting Results"
                    st.rerun()
                    
                if st.button("Snippets ▾", key=f"btn_snip_{meeting.id}", type="secondary", use_container_width=True):
                    st.session_state[f'show_snip_{meeting.id}'] = not st.session_state.get(f'show_snip_{meeting.id}', False)
                    st.rerun()
        
        if st.session_state.get(f'show_snip_{meeting.id}', False):
            st.markdown("<div style='margin-top: -0.5rem; margin-bottom: 1.5rem; padding: 1rem 1.5rem; background: rgba(255,255,255,0.4); border-radius: 0 0 16px 16px; border: 1px solid #E2E8F0; border-top: none;'>", unsafe_allow_html=True)
            for seg in segments[:5]: # show up to 5
                if search_query and search_query.lower() not in seg.text.lower():
                    continue
                m, s = divmod(int(seg.start), 60)
                h, m = divmod(m, 60)
                ts = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
                text = seg.text.replace(search_query, f"<b>{search_query}</b>") if search_query else seg.text
                transcript_message(seg.speaker, ts, text)
            if len(segments) > 5 and not search_query:
                st.markdown("<div style='text-align: center; color: var(--text-muted); font-size: 0.85rem;'>+ more segments... (Click View Meeting)</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

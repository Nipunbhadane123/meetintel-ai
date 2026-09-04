import streamlit as st
from storage.database import get_db
from storage.repository import get_all_meetings
from storage.models import TranscriptSegment

def render_transcripts_list():
    st.title("Transcript Library")
    
    db = next(get_db())
    meetings = get_all_meetings(db)
    
    if not meetings:
        st.info("No transcripts found.")
        return
        
    search_query = st.text_input("Search across all transcripts", "")
    
    for meeting in meetings:
        # Check if meeting has segments
        segments = db.query(TranscriptSegment).filter(TranscriptSegment.meeting_id == meeting.id).order_by(TranscriptSegment.start).all()
        if not segments:
            continue
            
        # If searching, filter meetings that match
        if search_query:
            match_found = any(search_query.lower() in s.text.lower() for s in segments)
            if not match_found:
                continue
                
        with st.expander(f"Transcript: {meeting.title} ({meeting.date.strftime('%Y-%m-%d')})"):
            st.markdown(f"**Duration:** {meeting.duration}s | **Speakers:** {meeting.speaker_count}")
            
            if st.button("View Full Meeting Results", key=f"btn_res_{meeting.id}"):
                st.session_state['current_meeting_id'] = meeting.id
                st.session_state['current_page'] = "Meeting Results"
                st.rerun()
                
            st.markdown("---")
            
            # Show transcript content
            for seg in segments:
                if search_query and search_query.lower() not in seg.text.lower():
                    continue
                    
                # Format Timestamp
                m, s = divmod(int(seg.start), 60)
                h, m = divmod(m, 60)
                if h > 0:
                    ts = f"[{h:02d}:{m:02d}:{s:02d}]"
                else:
                    ts = f"[{m:02d}:{s:02d}]"
                    
                # Highlight search term if present
                text = seg.text
                if search_query:
                    # Simple highlight (case insensitive match visually might be tricky without regex, keeping it simple)
                    text = text.replace(search_query, f"**{search_query}**")
                    
                st.markdown(f"**{ts} {seg.speaker}**")
                st.write(text)
                st.markdown("<br>", unsafe_allow_html=True)

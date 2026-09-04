import streamlit as st
from storage.database import get_db
from storage.repository import get_all_meetings
from storage.models import ActionItem, Speaker

def render_dashboard():
    st.header("Dashboard 👋")
    st.markdown("### Your Meeting Intelligence Overview")
    
    db = next(get_db())
    meetings = get_all_meetings(db)
    
    total_meetings = len(meetings)
    total_duration_sec = sum(m.duration for m in meetings) if meetings else 0
    total_hours = round(total_duration_sec / 3600, 2)
    
    total_action_items = db.query(ActionItem).count()
    total_speakers = db.query(Speaker).count()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Meetings", str(total_meetings))
    col2.metric("Total Meeting Hours", str(total_hours))
    col3.metric("Total Speakers", str(total_speakers))
    col4.metric("Action Items", str(total_action_items))
    
    st.markdown("### Recent Meetings")
    if not meetings:
        st.info("No recent meetings found. Go to 'New Meeting' to upload one.")
    else:
        for m in meetings[:5]: # Show top 5 recent
            with st.container():
                st.markdown(f"**{m.title}** ({m.date.strftime('%Y-%m-%d %H:%M')})")
                st.write(f"Status: {m.processing_status} | Duration: {m.duration}s")
                if m.executive_summary:
                    st.write(f"*{m.executive_summary[:150]}...*")
                
                if st.button("View Meeting", key=f"dash_btn_{m.id}"):
                    st.session_state['current_meeting_id'] = m.id
                    st.session_state['current_page'] = "Meeting Results"
                    st.rerun()
                st.markdown("---")

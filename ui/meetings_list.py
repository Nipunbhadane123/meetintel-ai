import streamlit as st
import pandas as pd
from storage.database import get_db
from storage.repository import get_all_meetings

def render_meetings_list():
    st.title("All Meetings")
    
    db = next(get_db())
    meetings = get_all_meetings(db)
    
    if not meetings:
        st.info("No meetings found. Go to 'New Meeting' to transcribe one.")
        return
        
    for m in meetings:
        with st.expander(f"{m.title} - {m.date.strftime('%Y-%m-%d %H:%M')}"):
            st.write(f"**Duration:** {m.duration} seconds")
            st.write(f"**Status:** {m.processing_status}")
            if st.button("View Results", key=f"btn_{m.id}"):
                st.session_state['current_meeting_id'] = m.id
                st.session_state['current_page'] = "Meeting Results"
                st.rerun()

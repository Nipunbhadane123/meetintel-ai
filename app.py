import streamlit as st
import os
from dotenv import load_dotenv

from storage.database import init_db

# Load environment variables
load_dotenv()

# Import models to ensure they are registered with Base
import storage.models

# Initialize Database
init_db()

st.set_page_config(
    page_title="MeetIntel AI",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import apply_global_styles
from ui.navigation import render_sidebar_navigation

def main():
    apply_global_styles()
    
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Dashboard"
        
    render_sidebar_navigation()
        
    page = st.session_state['current_page']
    
    if page == "Dashboard":
        from ui.dashboard import render_dashboard
        render_dashboard()
    elif page == "New Meeting":
        from ui.upload import render_upload_page
        render_upload_page()
    elif page == "Processing":
        from ui.meeting import render_processing_page
        render_processing_page()
    elif page == "Meetings":
        from ui.meetings_list import render_meetings_list
        render_meetings_list()
    elif page == "Meeting Results":
        if 'current_meeting_id' not in st.session_state:
            st.error("No active meeting.")
            return
            
        meeting_id = st.session_state['current_meeting_id']
        from storage.database import get_db
        from storage.repository import get_meeting
        
        db = next(get_db())
        meeting = get_meeting(db, meeting_id)
        
        if not meeting:
            st.error("Meeting not found.")
            return
            
        from ui.components import section_header
        duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s"
        subtitle = f"📅 {meeting.date.strftime('%Y-%m-%d')} • ⏱️ {duration_str} • 👥 {meeting.speaker_count} Speakers"
        
        # Display Header
        st.markdown(f"""
            <div class="page-title-container" style="display: flex; justify-content: space-between; align-items: flex-end;">
                <div>
                    <h2 class="page-title">📄 {meeting.title}</h2>
                    <p class="page-subtitle">{subtitle}</p>
                </div>
                <span class="badge badge-completed" style="font-size: 0.9rem;">✓ {meeting.processing_status}</span>
            </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Overview", "Action Items", "Participants", "Deadlines", "Priorities", "Transcript", "Ask AI", "MoM"])
        
        with tab1:
            from ui.insights_view import render_insights_tab
            render_insights_tab(meeting)
            
        with tab2:
            from ui.action_items import render_action_items_tab
            render_action_items_tab(meeting.id)
            
        with tab3:
            from ui.participants_view import render_participants_tab
            render_participants_tab(meeting.id)
            
        with tab4:
            from ui.deadlines_view import render_deadlines_tab
            render_deadlines_tab(meeting.id)
            
        with tab5:
            from ui.priorities_view import render_priorities_tab
            render_priorities_tab(meeting.id)
            
        with tab6:
            from ui.transcript_view import render_transcript_tab
            render_transcript_tab(meeting.id)
            
        with tab7:
            from ui.ask_ai import render_ask_ai_tab
            render_ask_ai_tab(meeting.id)
            
        with tab8:
            from ui.mom import render_mom_tab
            render_mom_tab(meeting)
            
    elif page == "Transcripts":
        from ui.transcripts_list import render_transcripts_list
        render_transcripts_list()
        
    elif page == "Settings":
        from ui.settings import render_settings_page
        render_settings_page()
            
    else:
        st.info(f"Page '{page}' is under construction.")
    
if __name__ == "__main__":
    main()

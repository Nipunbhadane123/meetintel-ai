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

def main():
    st.title("MeetIntel AI")
    st.markdown("### AI-Powered Meeting Intelligence")
    
    # Initialize session state for navigation
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "Dashboard"
        
    st.sidebar.title("MeetIntel AI")
    
    # Sidebar navigation
    pages = ["Dashboard", "New Meeting", "Meetings", "Transcripts", "Settings"]
    
    # Use radio button, but handle internal pages gracefully
    internal_pages = ["Processing", "Meeting Results"]
    current_page = st.session_state.get('current_page', 'Dashboard')

    # Find a safe index for the radio button (visual only)
    visual_index = pages.index(current_page) if current_page in pages else 0

    selected_page = st.sidebar.radio(
        "Navigation",
        pages,
        index=visual_index
    )
    # If the user clicked the sidebar to change pages, override the internal state
    if selected_page != (current_page if current_page in pages else pages[visual_index]):
        st.session_state['current_page'] = selected_page
        st.rerun()
        
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
            
        st.title(f"Results: {meeting.title}")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Overview & Insights", "Transcript", "Action Items", "Ask AI", "MoM"])
        
        with tab1:
            from ui.insights_view import render_insights_tab
            render_insights_tab(meeting)
            
        with tab2:
            from ui.transcript_view import render_transcript_tab
            render_transcript_tab(meeting.id)
            
        with tab3:
            from ui.action_items import render_action_items_tab
            render_action_items_tab(meeting.id)
            
        with tab4:
            from ui.ask_ai import render_ask_ai_tab
            render_ask_ai_tab(meeting.id)
            
        with tab5:
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

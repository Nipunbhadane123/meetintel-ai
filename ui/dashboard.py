import streamlit as st
from storage.database import get_db, SessionLocal
from storage.repository import get_all_meetings
from storage.models import ActionItem, Speaker
from ui.components import metric_card, render_meeting_card, section_header, empty_state
import datetime

def render_dashboard():
    # Hero Section
    current_hour = datetime.datetime.now().hour
    greeting = "Good morning" if current_hour < 12 else "Good afternoon" if current_hour < 18 else "Good evening"
    
    st.markdown(f"""
        <div style="position: relative; overflow: hidden; background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-xl); padding: var(--mt-space-2xl); margin-bottom: var(--mt-space-xl); box-shadow: var(--mt-shadow-soft); display: flex; justify-content: space-between; align-items: center;">
            <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: radial-gradient(circle, rgba(109,61,245,0.15) 0%, transparent 70%); border-radius: 50%; filter: blur(30px); z-index: 0;"></div>
            <div style="position: absolute; bottom: -30px; left: 10%; width: 150px; height: 150px; background: radial-gradient(circle, rgba(79,70,229,0.1) 0%, transparent 70%); border-radius: 50%; filter: blur(20px); z-index: 0;"></div>
            <div style="z-index: 1;">
                <h1 style="font-size: 2.2rem; font-weight: 750; color: var(--mt-text); margin-bottom: var(--mt-space-xs); letter-spacing: -0.02em;">{greeting},<br/>welcome to MeetIntel AI</h1>
                <p style="color: var(--mt-text-secondary); font-size: 1.1rem; margin: 0; font-weight: 500;">Turn every meeting into searchable, actionable knowledge.</p>
            </div>
            <div style="z-index: 1; font-size: 3.5rem; background: var(--mt-grad-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0px 8px 16px rgba(109,61,245,0.2));">✦</div>
        </div>
    """, unsafe_allow_html=True)
    
    db = next(get_db())
    meetings = get_all_meetings(db)
    
    total_meetings = len(meetings)
    total_action_items = db.query(ActionItem).count()
    
    # Get indexed knowledge count
    from storage.knowledge import get_knowledge_repository
    try:
        repo = get_knowledge_repository()
        total_vectors = repo.vector_store.collection.count()
    except Exception:
        total_vectors = 0
    
    # Render Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Meetings", str(total_meetings), "◈", "Meetings processed")
    with col2:
        metric_card("Total Transcripts", str(total_meetings), "☶", "Audio files transcribed")
    with col3:
        metric_card("Action Items", str(total_action_items), "✓", "Tasks generated")
    with col4:
        metric_card("Indexed Knowledge", str(total_vectors), "✧", "Vector chunks available")
        
    st.markdown("<div style='height: var(--mt-space-xl);'></div>", unsafe_allow_html=True)
    
    # Quick Actions & Recent Meetings Layout
    left_col, right_col = st.columns([3, 1])
    
    with left_col:
        st.markdown("<h3 style='font-size: 1.25rem; font-weight: 650; color: var(--mt-text); margin-bottom: var(--mt-space-md);'>Recent Meetings</h3>", unsafe_allow_html=True)
        if not meetings:
            empty_state("📭", "No meetings yet", "Upload your first meeting to start generating intelligence.")
        else:
            for m in meetings[:4]: # Show top 4 recent
                render_meeting_card(m, button_key=f"dash_btn_{m.id}")
                
    with right_col:
        st.markdown("<h3 style='font-size: 1.25rem; font-weight: 650; color: var(--mt-text); margin-bottom: var(--mt-space-md);'>Quick Actions</h3>", unsafe_allow_html=True)
        
        if st.button("＋ Upload New Meeting", key="qa_upload", use_container_width=True, type="primary"):
            st.session_state['current_page'] = "New Meeting"
            st.rerun()
            
        if st.button("✧ Search Knowledge", key="qa_search", use_container_width=True):
            st.session_state['current_page'] = "Knowledge Search"
            st.rerun()
            
        if st.button("⚙ View Settings", key="qa_settings", use_container_width=True):
            st.session_state['current_page'] = "Settings"
            st.rerun()

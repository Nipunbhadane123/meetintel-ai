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
        <div style="position: relative; overflow: hidden; background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-xl); padding: var(--mt-space-2xl); margin-bottom: var(--mt-space-xl); box-shadow: var(--mt-shadow-card); display: flex; justify-content: space-between; align-items: center;">
            <div style="position: absolute; top: -100px; right: -50px; width: 300px; height: 300px; background: radial-gradient(circle, rgba(108,76,241,0.12) 0%, transparent 70%); border-radius: 50%; filter: blur(40px); z-index: 0;"></div>
            <div style="position: absolute; bottom: -50px; left: 5%; width: 200px; height: 200px; background: radial-gradient(circle, rgba(6,182,212,0.08) 0%, transparent 70%); border-radius: 50%; filter: blur(30px); z-index: 0;"></div>
            <div style="z-index: 1;">
                <h1 style="font-size: 2.4rem; font-weight: 700; color: var(--mt-text); margin-bottom: 8px; letter-spacing: -0.02em;">{greeting},<br/>welcome to MeetIntel AI</h1>
                <p style="color: var(--mt-text-secondary); font-size: 1.1rem; margin: 0; font-weight: 400; line-height: 1.5;">Turn every meeting into searchable, actionable knowledge.</p>
            </div>
            <div style="z-index: 1; font-size: 4rem; background: var(--mt-grad-primary); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0px 8px 16px rgba(108,76,241,0.2)); opacity: 0.9;">✦</div>
        </div>
    """, unsafe_allow_html=True)
    
    user_id = st.session_state.get('user_id')
    db = next(get_db())
    
    try:
        meetings = get_all_meetings(db, user_id=user_id)
        total_meetings = len(meetings)
        
        # Total action items for this user's meetings
        meeting_ids = [m.id for m in meetings]
        if meeting_ids:
            total_action_items = db.query(ActionItem).filter(ActionItem.meeting_id.in_(meeting_ids)).count()
            # Get upcoming deadlines
            from storage.models import Deadline
            upcoming_deadlines = db.query(Deadline).filter(Deadline.meeting_id.in_(meeting_ids)).limit(3).all()
        else:
            total_action_items = 0
            upcoming_deadlines = []
            
        # Get indexed knowledge count
        from storage.knowledge import get_knowledge_repository
        try:
            repo = get_knowledge_repository()
            # Must isolate by user_id to prevent leaking global knowledge sizes
            if user_id:
                results = repo.vector_store.collection.get(where={"user_id": user_id}, include=[])
                total_vectors = len(results["ids"])
            else:
                total_vectors = 0
        except Exception:
            total_vectors = 0
            
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Dashboard Database Error: {e}")
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid var(--mt-error); border-radius: var(--mt-radius-md); padding: 16px; margin-bottom: 24px;">
            <h3 style="color: var(--mt-error); margin-top: 0; margin-bottom: 8px;">Database Connection Error</h3>
            <p style="color: var(--mt-error); margin-bottom: 16px;">Unable to load meetings right now. Please try again.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Retry", key="dash_retry", type="primary"):
            st.rerun()
        return
    
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
            for m in meetings[:3]: # Show top 3 recent
                render_meeting_card(m, button_key=f"dash_btn_{m.id}")
                
        st.markdown("<h3 style='font-size: 1.25rem; font-weight: 650; color: var(--mt-text); margin-top: var(--mt-space-xl); margin-bottom: var(--mt-space-md);'>Upcoming Deadlines</h3>", unsafe_allow_html=True)
        if not upcoming_deadlines:
            st.info("No upcoming deadlines.")
        else:
            for dl in upcoming_deadlines:
                st.markdown(f"""
                <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-md); padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between;">
                    <div><strong>{dl.description}</strong><br/><small style="color: var(--mt-text-secondary);">{dl.related_task}</small></div>
                    <div style="color: var(--mt-primary); font-weight: 600;">{dl.date}</div>
                </div>
                """, unsafe_allow_html=True)
                
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

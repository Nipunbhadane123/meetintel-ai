import streamlit as st
from storage.database import get_db
from storage.repository import get_all_meetings
from storage.models import ActionItem, Speaker
from ui.components import metric_card, render_meeting_card, section_header, empty_state

def render_dashboard():
    # Centered Header
    st.markdown("""
        <div style="text-align: center; margin-bottom: 3rem;">
            <h1 class="gradient-text" style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">MeetIntel AI</h1>
            <p style="color: var(--text-muted); font-size: 1.1rem;">AI-Powered Meeting Intelligence</p>
        </div>
    """, unsafe_allow_html=True)
    
    section_header("👋 Dashboard", "Your meeting intelligence overview")
    
    db = next(get_db())
    meetings = get_all_meetings(db)
    
    total_meetings = len(meetings)
    total_duration_sec = sum(m.duration for m in meetings) if meetings else 0
    total_hours = round(total_duration_sec / 3600, 2)
    
    total_action_items = db.query(ActionItem).count()
    total_speakers = db.query(Speaker).count()
    
    # Render Metric Cards in identical columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Meetings", str(total_meetings), "🎙️", "Meetings recorded")
    with col2:
        metric_card("Total Hours", str(total_hours), "⏱️", "Hours of audio processed")
    with col3:
        metric_card("Total Speakers", str(total_speakers), "👥", "Unique speakers identified")
    with col4:
        metric_card("Action Items", str(total_action_items), "✅", "Tasks generated")
        
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("Recent Meetings", "Your latest processed meetings")
    
    if not meetings:
        empty_state("📭", "No meetings yet", "Upload your first meeting to start generating intelligence.")
    else:
        for m in meetings[:5]: # Show top 5 recent
            render_meeting_card(m, button_key=f"dash_btn_{m.id}")

    # Capabilities Section
    st.markdown("<br>", unsafe_allow_html=True)
    section_header("✨ Platform Capabilities", "What MeetIntel AI can do for you")
    
    cap_col1, cap_col2, cap_col3, cap_col4 = st.columns(4)
    capabilities = [
        ("🎙️", "AI Transcription", "Convert speech to accurate text"),
        ("👥", "Speaker Diarization", "Identify who said what"),
        ("✦", "Smart Insights", "Extract decisions and action items"),
        ("📄", "Meeting Reports", "Generate professional meeting reports")
    ]
    
    for col, (icon, title, desc) in zip([cap_col1, cap_col2, cap_col3, cap_col4], capabilities):
        with col:
            st.markdown(f"""
            <div class="saas-card" style="text-align: center; padding: 1.5rem 1rem;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>
                <h4 style="font-size: 1rem; color: var(--text-main); margin-bottom: 0.5rem; font-weight: 600;">{title}</h4>
                <p style="font-size: 0.8rem; color: var(--text-muted); margin: 0;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

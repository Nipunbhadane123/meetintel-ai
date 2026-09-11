import streamlit as st

def render_sidebar_navigation():
    # Sidebar Header
    st.sidebar.markdown("""
        <div class="sidebar-logo-container">
            <h1 class="sidebar-logo-title">MeetIntel AI</h1>
            <div class="sidebar-logo-subtitle">AI-Powered Meeting Intelligence</div>
        </div>
        <hr style="margin-top: 0.5rem; margin-bottom: 1.5rem; border-color: rgba(0,0,0,0.05);">
    """, unsafe_allow_html=True)
    
    # Navigation Items
    nav_items = [
        {"name": "Dashboard", "icon": "👋"},
        {"name": "New Meeting", "icon": "🎙️"},
        {"name": "Meetings", "icon": "📂"},
        {"name": "Transcripts", "icon": "📄"},
        {"name": "Settings", "icon": "⚙️"}
    ]
    
    current_page = st.session_state.get('current_page', 'Dashboard')
    
    for item in nav_items:
        is_active = current_page == item["name"]
        
        # Use a button styled to look like a nav item
        # We'll use a hack to style a specific button by injecting CSS, or just rely on st.button
        if st.sidebar.button(f"{item['icon']} {item['name']}", key=f"nav_{item['name']}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state['current_page'] = item["name"]
            st.rerun()
            
    # Bottom section for user/profile - FIX OVERLAPPING BUG BY REMOVING ABSOLUTE POSITIONING
    st.sidebar.markdown("""
        <div style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.05); text-align: center;">
            <div style="font-size: 0.8rem; color: #64748B;">MeetIntel AI v2.0</div>
        </div>
    """, unsafe_allow_html=True)

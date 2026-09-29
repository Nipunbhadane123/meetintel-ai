import streamlit as st

def render_sidebar_navigation():
    # Sidebar Header
    st.sidebar.markdown("""
        <div class="sidebar-logo-container">
            <div class="sidebar-logo-icon">✧</div>
            <div class="sidebar-logo-text">
                <div class="sidebar-logo-title">MeetIntel AI</div>
                <div class="sidebar-logo-subtitle">Knowledge Platform</div>
            </div>
        </div>
        <div style="height: 24px;"></div>
    """, unsafe_allow_html=True)
    
    # Navigation Items
    nav_items = [
        {"name": "Dashboard", "icon": "◈"},
        {"name": "New Meeting", "icon": "＋"},
        {"name": "Meetings", "icon": "✤"},
        {"name": "Transcripts", "icon": "☶"},
        {"name": "Knowledge Search", "icon": "✧"},
        {"name": "Settings", "icon": "⏣"}
    ]
    
    current_page = st.session_state.get('current_page', 'Dashboard')
    
    for item in nav_items:
        is_active = current_page == item["name"]
        
        # Use primary for active, secondary for inactive
        if st.sidebar.button(f"{item['icon']} \u00A0 {item['name']}", key=f"nav_{item['name']}", use_container_width=True, type="primary" if is_active else "secondary"):
            st.session_state['current_page'] = item["name"]
            st.rerun()
            
    st.sidebar.markdown("""
        <div style="margin-top: auto; padding-top: 32px; padding-left: 12px;">
            <div style="font-size: 0.75rem; color: var(--mt-text-muted); font-weight: 500;">MeetIntel AI v2.0</div>
        </div>
    """, unsafe_allow_html=True)

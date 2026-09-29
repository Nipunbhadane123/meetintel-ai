import streamlit as st
import pandas as pd
from storage.database import get_db, SessionLocal
from storage.repository import get_all_meetings
from ui.components import render_meeting_card, empty_state

def render_meetings_list():
    st.markdown("""
        <div class="page-title-container" style="margin-bottom: var(--mt-space-xl);">
            <h2 class="page-title" style="color: var(--mt-text); font-weight: 750; font-size: 2.2rem; margin: 0 0 8px 0; letter-spacing: -0.02em;"><span style="color: var(--mt-primary);">✤</span> Meeting Library</h2>
            <p class="page-subtitle" style="color: var(--mt-text-secondary); font-size: 1.1rem; margin: 0;">Browse and search your processed meetings.</p>
        </div>
    """, unsafe_allow_html=True)
    
    db = SessionLocal()
    meetings = get_all_meetings(db)
    
    if not meetings:
        empty_state("📭", "No meetings found", "Upload a meeting to see it here.")
    else:
        # Search Box
        search_query = st.text_input("Search meetings by title...", label_visibility="collapsed", placeholder="🔍 Search meetings by title...")
        st.markdown("<div style='height: var(--mt-space-lg);'></div>", unsafe_allow_html=True)
        
        filtered_meetings = [m for m in meetings if not search_query or search_query.lower() in m.title.lower()]
        
        if not filtered_meetings:
            st.info("No meetings match your search.")
        else:
            for m in filtered_meetings:
                render_meeting_card(m, button_key=f"btn_{m.id}")
                
    db.close()

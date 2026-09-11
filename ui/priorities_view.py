import streamlit as st
from storage.database import get_db
from storage.models import Priority
from ui.components import section_header, empty_state

def render_priorities_tab(meeting_id):
    section_header("📌 Priorities", "Prioritized items from the meeting")
    
    db = next(get_db())
    priorities = db.query(Priority).filter(Priority.meeting_id == meeting_id).all()
    
    if not priorities:
        empty_state("📌", "No priorities", "No explicit priorities were identified in this meeting.")
        return
        
    for p in priorities:
        priority_color = "var(--primary)"
        if "high" in p.priority_level.lower():
            priority_color = "var(--error)"
        elif "low" in p.priority_level.lower():
            priority_color = "var(--success)"
            
        html = f"""
        <div class="saas-card" style="border-left: 4px solid {priority_color}; margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="color: var(--text-main); margin: 0;">{p.item}</h4>
                <span class="badge" style="background: {priority_color}20; color: {priority_color}; padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.85rem; font-weight: 600;">{p.priority_level}</span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

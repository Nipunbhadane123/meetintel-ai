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
        priority_color = "var(--mt-primary)"
        if "high" in p.priority_level.lower():
            priority_color = "var(--mt-error)"
        elif "low" in p.priority_level.lower():
            priority_color = "var(--mt-success)"
            
        html = f"""
        <div class="saas-card" style="border-left: 4px solid {priority_color}; margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h4 style="color: var(--mt-text); margin: 0; font-weight: 650; font-size: 1.1rem;">{p.item}</h4>
                <span class="badge" style="background: rgba(0,0,0,0.04); color: {priority_color}; padding: 6px 12px; border-radius: var(--mt-radius-sm); font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(0,0,0,0.05);">{p.priority_level}</span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

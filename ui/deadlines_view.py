import streamlit as st
import pandas as pd
from storage.database import get_db
from storage.models import Deadline
from ui.components import section_header, empty_state

def render_deadlines_tab(meeting_id):
    section_header("📅 Deadlines", "Key dates and deadlines mentioned")
    
    db = next(get_db())
    deadlines = db.query(Deadline).filter(Deadline.meeting_id == meeting_id).all()
    
    if not deadlines:
        empty_state("📅", "No deadlines", "No explicit deadlines were identified in this meeting.")
        return
        
    for dl in deadlines:
        html = f"""
        <div class="saas-card" style="border-left: 4px solid var(--primary); margin-bottom: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <h4 style="color: var(--text-main); margin-bottom: 0.25rem;">{dl.description}</h4>
                    <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 0;">Task: {dl.related_task}</p>
                </div>
                <div style="text-align: right;">
                    <span class="badge badge-primary" style="font-size: 0.85rem;">{dl.date}</span>
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

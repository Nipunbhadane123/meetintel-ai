import streamlit as st
import html
from storage.database import get_db
from storage.models import Priority
from ui.components import section_header, empty_state, render_status_badge, safe_escape, get_icon_svg

def render_priorities_tab(meeting_id):
    section_header("Priorities & Urgency Classifications", "Prioritized strategic initiatives and urgency classifications identified in dialogue.", category="Meeting Deliverables")
    
    db = next(get_db())
    priorities = db.query(Priority).filter(Priority.meeting_id == meeting_id).all()
    
    if not priorities:
        empty_state("target", "No priorities identified", "No explicit priorities were identified in this meeting.")
        return
        
    with st.container(border=True):
        for idx, p in enumerate(priorities):
            if idx > 0:
                st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 10px 0;'></div>", unsafe_allow_html=True)
            col_p1, col_p2 = st.columns([3.5, 1.2])
            with col_p1:
                st.markdown(f"<h4 style='color: var(--mt-text); margin: 0; font-weight: 700; font-size: 1.05rem;'>{safe_escape(p.item)}</h4>", unsafe_allow_html=True)
            with col_p2:
                st.markdown(f"<div style='text-align: right;'>{render_status_badge(p.priority_level, 'status')}</div>", unsafe_allow_html=True)

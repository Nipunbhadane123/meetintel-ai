import streamlit as st
import pandas as pd
import html
from storage.database import get_db
from storage.models import Deadline
from ui.components import section_header, empty_state, render_status_badge, safe_escape, get_icon_svg

def render_deadlines_tab(meeting_id):
    section_header("Deadlines & Milestones", "Key dates and confirmed timeframes mentioned in meeting dialogue.", category="Meeting Deliverables")
    
    db = next(get_db())
    deadlines = db.query(Deadline).filter(Deadline.meeting_id == meeting_id).all()
    
    if not deadlines:
        empty_state("calendar-clock", "No deadlines identified", "No explicit deadlines were identified in this meeting.")
        return
        
    with st.container(border=True):
        for idx, dl in enumerate(deadlines):
            if idx > 0:
                st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 10px 0;'></div>", unsafe_allow_html=True)
            col_d1, col_d2 = st.columns([3.5, 1.2])
            with col_d1:
                st.markdown(f"<h4 style='color: var(--mt-text); margin: 0 0 4px 0; font-weight: 700; font-size: 1.05rem;'>{safe_escape(dl.description)}</h4>", unsafe_allow_html=True)
                st.caption(f"Associated Commitment: {safe_escape(dl.related_task or 'General Deliverable')}")
            with col_d2:
                st.markdown(f"<div style='text-align: right;'>{render_status_badge(dl.date, 'status')}</div>", unsafe_allow_html=True)

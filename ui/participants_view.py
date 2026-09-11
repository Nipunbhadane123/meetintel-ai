import streamlit as st
import json
from storage.database import get_db
from storage.models import Participant
from ui.components import section_header, empty_state

def render_participants_tab(meeting_id):
    section_header("👥 Participants", "People identified in the meeting")
    
    db = next(get_db())
    participants = db.query(Participant).filter(Participant.meeting_id == meeting_id).all()
    
    if not participants:
        empty_state("👥", "No participants mapped", "Participant mapping hasn't been generated for this meeting.")
        return
        
    for p in participants:
        resp = []
        try:
            resp = json.loads(p.responsibilities) if p.responsibilities else []
        except:
            pass
            
        resp_html = ""
        if resp:
            resp_html = "<ul>" + "".join([f"<li>{r}</li>" for r in resp]) + "</ul>"
        else:
            resp_html = "<span style='color: var(--text-muted);'>No explicitly assigned responsibilities.</span>"
            
        html = f"""
        <div class="saas-card" style="margin-bottom: 1rem;">
            <h4 style="color: var(--text-main); margin-bottom: 0.25rem;">{p.name}</h4>
            <p style="color: var(--text-muted); font-size: 0.85rem; margin-bottom: 1rem;">Speaker ID: {p.speaker_id}</p>
            <div style="font-size: 0.9rem;">
                <strong>Responsibilities:</strong>
                <div style="margin-top: 0.5rem; padding-left: 0.5rem;">
                    {resp_html}
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

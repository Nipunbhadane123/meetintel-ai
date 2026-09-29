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
            resp_html = "<ul style='padding-left: 20px; color: var(--mt-text-secondary); line-height: 1.6; margin: 0;'>" + "".join([f"<li style='margin-bottom: 6px;'>{r}</li>" for r in resp]) + "</ul>"
        else:
            resp_html = "<span style='color: var(--mt-text-muted);'>No explicitly assigned responsibilities.</span>"
            
        html = f"""
        <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                <div style="width: 40px; height: 40px; border-radius: 50%; background: var(--mt-surface-soft); border: 1px solid var(--mt-border); display: flex; align-items: center; justify-content: center; font-weight: 600; color: var(--mt-primary);">{p.name[0].upper() if p.name else "?"}</div>
                <div>
                    <h4 style="color: var(--mt-text); margin: 0; font-weight: 650; font-size: 1.1rem;">{p.name}</h4>
                    <p style="color: var(--mt-text-muted); font-size: 0.85rem; margin: 0;">Speaker ID: {p.speaker_id}</p>
                </div>
            </div>
            <div style="font-size: 0.95rem; margin-top: var(--mt-space-md);">
                <strong style="color: var(--mt-text); display: block; margin-bottom: 8px;">Responsibilities:</strong>
                <div style="margin-top: 0.5rem; padding-left: 0.5rem;">
                    {resp_html}
                </div>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

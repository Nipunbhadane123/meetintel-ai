import streamlit as st
import json
import html
from storage.database import get_db
from storage.models import Participant
from ui.components import section_header, empty_state, safe_escape, get_icon_svg

def render_participants_tab(meeting_id):
    section_header("Participants & Speaker Mapping", "People identified in the session and attributed responsibilities.", category="Meeting Dossier")
    
    db = next(get_db())
    participants = db.query(Participant).filter(Participant.meeting_id == meeting_id).all()
    
    if not participants:
        empty_state("users", "No participants mapped", "Participant mapping hasn't been generated for this meeting.")
        return
        
    with st.container(border=True):
        for idx, p in enumerate(participants):
            if idx > 0:
                st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 12px 0;'></div>", unsafe_allow_html=True)
            resp = []
            try:
                resp = json.loads(p.responsibilities) if p.responsibilities else []
            except:
                pass
                
            col_avatar, col_info = st.columns([0.4, 6])
            with col_avatar:
                initial = (p.name[0] if p.name else "?").upper()
                st.markdown(f"<div style='width: 38px; height: 38px; border-radius: 50%; background: var(--mt-primary-light); color: var(--mt-primary); display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.95rem;'>{safe_escape(initial)}</div>", unsafe_allow_html=True)
            with col_info:
                st.markdown(f"<h4 style='color: var(--mt-text); margin: 0; font-weight: 700; font-size: 1.05rem;'>{safe_escape(p.name)}</h4>", unsafe_allow_html=True)
                st.caption(f"Speaker Diarization Tag: {safe_escape(p.speaker_id)}")

                if resp:
                    st.markdown("<strong style='font-size: 0.8rem; color: var(--mt-text-secondary); text-transform: uppercase;'>Attributed Responsibilities:</strong>", unsafe_allow_html=True)
                    for r in resp:
                        st.markdown(f"<div style='font-size: 0.88rem; color: var(--mt-text); padding: 1px 0;'>• {safe_escape(r)}</div>", unsafe_allow_html=True)
                else:
                    st.caption("No explicitly assigned commitments recorded.")

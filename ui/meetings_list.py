import streamlit as st
import pandas as pd
from storage.database import get_db
from storage.repository import get_all_meetings
from ui.components import section_header, render_meeting_card, empty_state

def render_meetings_list():
    section_header("📂 Meeting Library", "Browse and search your processed meetings")
    
    db = next(get_db())
    meetings = get_all_meetings(db)
    
    if not meetings:
        empty_state("📭", "No meetings found", "Upload a meeting to see it here.")
        return
        
    for m in meetings:
        render_meeting_card(m, button_key=f"btn_{m.id}")

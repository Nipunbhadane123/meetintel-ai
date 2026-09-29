import streamlit as st
import pandas as pd
from storage.database import get_db
from storage.models import ActionItem
from ui.components import section_header, empty_state

def render_action_items_tab(meeting_id):
    section_header("✅ Action Items", "Tasks identified during the meeting")
    
    db = next(get_db())
    items = db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).all()
    
    if not items:
        empty_state("✅", "No action items", "No action items were identified in this meeting.")
        return
        
    for item in items:
        # Determine badge color for priority
        priority_color = "var(--mt-primary)" # Default
        if "high" in (item.priority or "").lower():
            priority_color = "var(--mt-error)"
        elif "low" in (item.priority or "").lower():
            priority_color = "var(--mt-success)"
            
        html = f"""
        <div class="saas-card" style="border-left: 4px solid {priority_color}; padding: var(--mt-space-lg) var(--mt-space-xl); margin-bottom: var(--mt-space-md);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: var(--mt-space-sm);">
                <h4 style="color: var(--mt-text); margin: 0; font-size: 1.1rem; font-weight: 650;">{item.task}</h4>
                <span class="badge badge-pending" style="font-size: 0.75rem;">{item.status}</span>
            </div>
            <div style="display: flex; gap: var(--mt-space-xl); color: var(--mt-text-secondary); font-size: 0.9rem; margin-top: var(--mt-space-md);">
                <span style="display: flex; align-items: center; gap: 6px;">👤 Assigned To: <strong style="color: var(--mt-text);">{item.assigned_to or 'Unassigned'}</strong></span>
                <span style="display: flex; align-items: center; gap: 6px;">📅 Deadline: <strong style="color: var(--mt-text);">{item.deadline or 'None'}</strong></span>
                <span style="display: flex; align-items: center; gap: 6px;">📌 Priority: <strong style="color: {priority_color};">{item.priority or 'Normal'}</strong></span>
            </div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    csv = pd.DataFrame([{ "Task": i.task, "Assigned To": i.assigned_to, "Deadline": i.deadline, "Priority": i.priority, "Status": i.status } for i in items]).to_csv(index=False)
    st.download_button("↓ Download Action Items (CSV)", data=csv, file_name=f"ActionItems_{meeting_id}.csv", mime="text/csv", type="secondary")

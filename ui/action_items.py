import streamlit as st
import json
import pandas as pd
import html
from storage.database import get_db
from storage.models import ActionItem, User
from storage import repository
from ui.components import section_header, empty_state, render_task_card, metric_card

def render_action_items_tab(meeting_id):
    section_header("Action Items & Task Execution", "Convert meeting commitments into approved, accountable work.", category="Meeting Deliverables")
    
    db = next(get_db())
    current_user_id = st.session_state.get('user_id')
    current_user = repository.get_user_by_id(db, current_user_id) if current_user_id else None
    user_role = current_user.role if current_user else "Employee"
    org_id = current_user.org_id if current_user else "org-default-001"

    items = db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).all()
    
    if not items:
        empty_state("check-circle", "No action items", "No action items were identified in this meeting.")
        return

    # Filter / Overview Stats using refined metric cards
    total = len(items)
    approved = sum(1 for i in items if i.approval_status == "Approved")
    pending = sum(1 for i in items if i.approval_status != "Approved")
    completed = sum(1 for i in items if i.status == "Completed")
    
    col_st1, col_st2, col_st3, col_st4 = st.columns(4)
    with col_st1:
        metric_card("Total Identified", str(total), "list-check", "Extracted tasks")
    with col_st2:
        metric_card("Leadership Approved", str(approved), "check-circle", "Signed off")
    with col_st3:
        metric_card("Awaiting Sign-off", str(pending), "clock", "Needs review")
    with col_st4:
        metric_card("Delivered", str(completed), "target", "Completed work")
            
    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    for item in items:
        render_task_card(item, db, current_user_id, user_role, is_blocked=(item.status == "Blocked"), show_meeting=False)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    csv = pd.DataFrame([{
        "Task": i.task,
        "Description": i.description,
        "Assigned To": i.assigned_to,
        "Assignment Status": i.assignment_status,
        "Deadline": i.deadline,
        "Priority": i.priority,
        "Status": i.status,
        "Approval Status": i.approval_status,
        "Confidence": i.confidence,
        "Evidence Excerpt": i.evidence_excerpt
    } for i in items]).to_csv(index=False)
    st.download_button("↓ Export Verified Action Items (CSV)", data=csv, file_name=f"ActionItems_{meeting_id}.csv", mime="text/csv", type="secondary")

import streamlit as st
import pandas as pd
from storage.database import get_db
from storage.models import ActionItem

def render_action_items_tab(meeting_id):
    st.header("Action Items")
    
    db = next(get_db())
    items = db.query(ActionItem).filter(ActionItem.meeting_id == meeting_id).all()
    
    if not items:
        st.info("No action items detected in this meeting.")
        return
        
    # Convert to DataFrame for interactive table
    data = []
    for item in items:
        data.append({
            "Task": item.task,
            "Owner": item.owner,
            "Deadline": item.deadline,
            "Priority": item.priority,
            "Status": item.status
        })
        
    df = pd.DataFrame(data)
    
    # Render interactive dataframe
    st.dataframe(df, use_container_width=True, hide_index=True)

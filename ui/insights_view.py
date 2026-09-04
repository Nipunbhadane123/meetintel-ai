import streamlit as st
import json

def render_insights_tab(meeting):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.header("Executive Summary")
    with col2:
        insights_data = {
            "executive_summary": meeting.executive_summary,
            "meeting_objective": meeting.meeting_objective,
            "emotional_analysis": meeting.emotional_analysis,
            "key_topics": json.loads(meeting.key_topics) if meeting.key_topics else [],
            "key_points": json.loads(meeting.key_points) if meeting.key_points else [],
            "recommendations": json.loads(meeting.recommendations) if meeting.recommendations else [],
            "next_steps": json.loads(meeting.next_steps) if meeting.next_steps else []
        }
        st.download_button("Export Insights (JSON)", data=json.dumps(insights_data, indent=2), file_name=f"Insights_{meeting.id}.json", mime="application/json")
        
    st.write(meeting.executive_summary if meeting.executive_summary else "No summary available.")
    
    st.header("Meeting Objective")
    st.write(meeting.meeting_objective if meeting.meeting_objective else "Not explicitly identified.")
    
    st.header("Emotional Analysis")
    st.write(meeting.emotional_analysis if meeting.emotional_analysis else "Neutral")
    
    col1, col2 = st.columns(2)
    with col1:
        st.header("Key Topics")
        if meeting.key_topics:
            topics = json.loads(meeting.key_topics)
            for topic in topics:
                st.markdown(f"- {topic}")
        else:
            st.write("None")
            
        st.header("Key Points")
        if meeting.key_points:
            points = json.loads(meeting.key_points)
            for point in points:
                st.markdown(f"- {point}")
        else:
            st.write("None")
            
    with col2:
        st.header("Recommendations")
        if meeting.recommendations:
            recs = json.loads(meeting.recommendations)
            for rec in recs:
                st.markdown(f"- {rec}")
        else:
            st.write("None")
            
        st.header("Next Steps")
        if meeting.next_steps:
            steps = json.loads(meeting.next_steps)
            for step in steps:
                st.markdown(f"- {step}")
        else:
            st.write("None")

    st.header("Meeting Plan")
    st.write(meeting.meeting_plan if meeting.meeting_plan else "None")
    
    st.header("Risks and Issues")
    if meeting.risks:
        risks = json.loads(meeting.risks)
        for risk in risks:
            if isinstance(risk, dict):
                st.markdown(f"**{risk.get('risk', 'Unknown')}** (Impact: {risk.get('impact', 'Unknown')})")
                st.write(risk.get('context', ''))
                if risk.get('mitigation'):
                    st.write(f"Mitigation: {risk.get('mitigation')}")
            else:
                st.markdown(f"- {risk}")
    else:
        st.write("None")

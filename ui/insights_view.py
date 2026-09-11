import streamlit as st
import json
import html
from ui.components import section_header

def render_insights_tab(meeting):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        section_header("📊 Overview & Insights", "AI-generated analysis of your meeting")
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
        st.download_button("↓ Export (JSON)", data=json.dumps(insights_data, indent=2), file_name=f"Insights_{meeting.id}.json", mime="application/json", type="secondary")
        
    summary_text = html.escape(meeting.executive_summary) if meeting.executive_summary else "No summary available."
    st.markdown(f'''
    <div class="saas-card" style="background: linear-gradient(145deg, var(--surface), #F8FAFF); border-left: 4px solid var(--primary); margin-bottom: 1rem;">
        <h4 style="color: var(--text-main); margin-top: 0;">Executive Summary</h4>
        <p>{summary_text}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        obj_text = html.escape(meeting.meeting_objective) if meeting.meeting_objective else "Not explicitly identified."
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: 1rem;">
            <h4 style="color: var(--text-main); margin-top: 0;">🎯 Meeting Objective</h4>
            <p>{obj_text}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col_b:
        emo_text = html.escape(meeting.emotional_analysis) if meeting.emotional_analysis else "Neutral"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: 1rem;">
            <h4 style="color: var(--text-main); margin-top: 0;">🎭 Emotional Tone</h4>
            <p>{emo_text}</p>
        </div>
        ''', unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    with col1:
        topics = json.loads(meeting.key_topics) if meeting.key_topics else []
        topics_html = "<ul>" + "".join([f"<li>{html.escape(t)}</li>" for t in topics]) + "</ul>" if topics else "<p>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: 1rem;">
            <h4 style="color: var(--text-main); margin-top: 0;">🔑 Key Topics</h4>
            {topics_html}
        </div>
        ''', unsafe_allow_html=True)
            
        points = json.loads(meeting.key_points) if meeting.key_points else []
        points_html = "<ul>" + "".join([f"<li>{html.escape(p)}</li>" for p in points]) + "</ul>" if points else "<p>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: 1rem;">
            <h4 style="color: var(--text-main); margin-top: 0;">💡 Key Points</h4>
            {points_html}
        </div>
        ''', unsafe_allow_html=True)
            
    with col2:
        recs = json.loads(meeting.recommendations) if meeting.recommendations else []
        recs_html = "<ul>" + "".join([f"<li>{html.escape(r)}</li>" for r in recs]) + "</ul>" if recs else "<p>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: 1rem;">
            <h4 style="color: var(--text-main); margin-top: 0;">📌 Recommendations</h4>
            {recs_html}
        </div>
        ''', unsafe_allow_html=True)
            
        steps = json.loads(meeting.next_steps) if meeting.next_steps else []
        steps_html = "<ul>" + "".join([f"<li>{html.escape(s)}</li>" for s in steps]) + "</ul>" if steps else "<p>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: 1rem;">
            <h4 style="color: var(--text-main); margin-top: 0;">🚀 Next Steps</h4>
            {steps_html}
        </div>
        ''', unsafe_allow_html=True)
        
    plan_text = html.escape(meeting.meeting_plan) if meeting.meeting_plan else "None"
    st.markdown(f'''
    <div class="saas-card" style="margin-bottom: 1rem;">
        <h4 style="color: var(--text-main); margin-top: 0;">📅 Meeting Plan & Follow-up</h4>
        <p>{plan_text}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    risks_html = ""
    if meeting.risks:
        risks = json.loads(meeting.risks)
        for risk in risks:
            if isinstance(risk, dict):
                r_text = html.escape(risk.get('risk', 'Unknown'))
                imp = html.escape(risk.get('impact', 'Unknown'))
                ctx = html.escape(risk.get('context', ''))
                mit = html.escape(risk.get('mitigation', ''))
                risks_html += f"<div><strong>{r_text}</strong> (Impact: {imp})<br>{ctx}"
                if mit:
                    risks_html += f"<br><em>Mitigation:</em> {mit}"
                risks_html += "<hr></div>"
            else:
                risks_html += f"<ul><li>{html.escape(risk)}</li></ul>"
    if not risks_html:
        risks_html = "<p>None</p>"
        
    st.markdown(f'''
    <div class="saas-card" style="border-left: 4px solid var(--warning); margin-bottom: 1rem;">
        <h4 style="color: var(--text-main); margin-top: 0;">⚠️ Risks and Issues</h4>
        {risks_html}
    </div>
    ''', unsafe_allow_html=True)
    
    from storage.database import get_db
    from storage.models import Decision
    db = next(get_db())
    decisions = db.query(Decision).filter(Decision.meeting_id == meeting.id).all()
    dec_html = ""
    if decisions:
        for d in decisions:
            dec_html += f"<div><strong>{html.escape(d.decision)}</strong><br>{html.escape(d.context)}<hr></div>"
    else:
        dec_html = "<p>No decisions were identified.</p>"
        
    st.markdown(f'''
    <div class="saas-card" style="border-left: 4px solid var(--success); margin-bottom: 1rem;">
        <h4 style="color: var(--text-main); margin-top: 0;">🤝 Decisions</h4>
        {dec_html}
    </div>
    ''', unsafe_allow_html=True)

    # Show performance metrics if available
    if 'last_metrics' in st.session_state:
        metrics = st.session_state['last_metrics']
        st.markdown(f'''
        <div class="saas-card" style="margin-top: 2rem; background: #F8FAFC;">
            <h4 style="color: var(--text-main); margin-top: 0; font-size: 0.9rem;">⏱️ Processing Performance</h4>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.8rem; color: var(--text-muted);">
                <span>Audio Prep: <b>{metrics.get('audio', 0):.1f}s</b></span> |
                <span>Whisper: <b>{metrics.get('whisper', 0):.1f}s</b></span> |
                <span>Diarization: <b>{metrics.get('diarization', 0):.1f}s</b></span> |
                <span>Alignment: <b>{metrics.get('alignment', 0):.1f}s</b></span> |
                <span>AI Insights: <b>{metrics.get('llm', 0):.1f}s</b></span> |
                <span>Total: <b style="color: var(--primary);">{metrics.get('total', 0):.1f}s</b></span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

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
    <div style="background: var(--mt-surface); border: 1px solid var(--mt-border); border-radius: var(--mt-radius-xl); padding: var(--mt-space-xl); margin-bottom: var(--mt-space-lg); box-shadow: var(--mt-shadow-soft);">
        <h4 style="color: var(--mt-text); margin-top: 0; font-size: 1.25rem; font-weight: 650; margin-bottom: var(--mt-space-md);">Executive Summary</h4>
        <p style="color: var(--mt-text-secondary); font-size: 1.05rem; line-height: 1.7; margin: 0;">{summary_text}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        obj_text = html.escape(meeting.meeting_objective) if meeting.meeting_objective else "Not explicitly identified."
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">🎯 Meeting Objective</h4>
            <p style="color: var(--mt-text-secondary); line-height: 1.6; margin: 0;">{obj_text}</p>
        </div>
        ''', unsafe_allow_html=True)
    with col_b:
        emo_text = html.escape(meeting.emotional_analysis) if meeting.emotional_analysis else "Neutral"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">🎭 Emotional Tone</h4>
            <p style="color: var(--mt-text-secondary); line-height: 1.6; margin: 0;">{emo_text}</p>
        </div>
        ''', unsafe_allow_html=True)
        
    col1, col2 = st.columns(2)
    with col1:
        topics = json.loads(meeting.key_topics) if meeting.key_topics else []
        topics_html = "<ul style='padding-left: 20px; color: var(--mt-text-secondary); line-height: 1.6; margin: 0;'>" + "".join([f"<li style='margin-bottom: 8px;'>{html.escape(t)}</li>" for t in topics]) + "</ul>" if topics else "<p style='color: var(--mt-text-muted);'>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">🔑 Key Topics</h4>
            {topics_html}
        </div>
        ''', unsafe_allow_html=True)
            
        points = json.loads(meeting.key_points) if meeting.key_points else []
        points_html = "<ul style='padding-left: 20px; color: var(--mt-text-secondary); line-height: 1.6; margin: 0;'>" + "".join([f"<li style='margin-bottom: 8px;'>{html.escape(p)}</li>" for p in points]) + "</ul>" if points else "<p style='color: var(--mt-text-muted);'>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">💡 Key Points</h4>
            {points_html}
        </div>
        ''', unsafe_allow_html=True)
            
    with col2:
        recs = json.loads(meeting.recommendations) if meeting.recommendations else []
        recs_html = "<ul style='padding-left: 20px; color: var(--mt-text-secondary); line-height: 1.6; margin: 0;'>" + "".join([f"<li style='margin-bottom: 8px;'>{html.escape(r)}</li>" for r in recs]) + "</ul>" if recs else "<p style='color: var(--mt-text-muted);'>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">📌 Recommendations</h4>
            {recs_html}
        </div>
        ''', unsafe_allow_html=True)
            
        steps = json.loads(meeting.next_steps) if meeting.next_steps else []
        steps_html = "<ul style='padding-left: 20px; color: var(--mt-text-secondary); line-height: 1.6; margin: 0;'>" + "".join([f"<li style='margin-bottom: 8px;'>{html.escape(s)}</li>" for s in steps]) + "</ul>" if steps else "<p style='color: var(--mt-text-muted);'>None</p>"
        st.markdown(f'''
        <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
            <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">🚀 Next Steps</h4>
            {steps_html}
        </div>
        ''', unsafe_allow_html=True)
        
    plan_text = html.escape(meeting.meeting_plan) if meeting.meeting_plan else "None"
    st.markdown(f'''
    <div class="saas-card" style="margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
        <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">📅 Meeting Plan & Follow-up</h4>
        <p style="color: var(--mt-text-secondary); line-height: 1.6; margin: 0;">{plan_text}</p>
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
                risks_html += f"<div style='margin-bottom: 12px; color: var(--mt-text-secondary); line-height: 1.6;'><strong style='color: var(--mt-warning-dark);'>{r_text}</strong> (Impact: {imp})<br>{ctx}"
                if mit:
                    risks_html += f"<br><em>Mitigation:</em> {mit}"
                risks_html += "</div>"
            else:
                risks_html += f"<ul style='padding-left: 20px; color: var(--mt-text-secondary); margin: 0;'><li style='margin-bottom: 8px;'>{html.escape(risk)}</li></ul>"
    if not risks_html:
        risks_html = "<p style='color: var(--mt-text-muted);'>None</p>"
        
    st.markdown(f'''
    <div class="saas-card" style="border-left: 4px solid var(--mt-warning); margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
        <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">⚠️ Risks and Issues</h4>
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
            dec_html += f"<div style='margin-bottom: 12px; color: var(--mt-text-secondary); line-height: 1.6;'><strong style='color: var(--mt-success-dark);'>{html.escape(d.decision)}</strong><br>{html.escape(d.context)}</div>"
    else:
        dec_html = "<p style='color: var(--mt-text-muted);'>No decisions were identified.</p>"
        
    st.markdown(f'''
    <div class="saas-card" style="border-left: 4px solid var(--mt-success); margin-bottom: var(--mt-space-md); padding: var(--mt-space-lg);">
        <h4 style="color: var(--mt-text); margin-top: 0; font-weight: 650;">🤝 Decisions</h4>
        {dec_html}
    </div>
    ''', unsafe_allow_html=True)

    # Show performance metrics if available
    if 'last_metrics' in st.session_state:
        metrics = st.session_state['last_metrics']
        st.markdown(f'''
        <div style="background: var(--mt-surface-soft); border-radius: var(--mt-radius-lg); padding: var(--mt-space-md) var(--mt-space-lg); margin-top: var(--mt-space-2xl); border: 1px solid var(--mt-border);">
            <h4 style="color: var(--mt-text); margin-top: 0; margin-bottom: 8px; font-size: 0.95rem; font-weight: 600;">⏱️ Processing Performance</h4>
            <div style="display: flex; gap: 16px; flex-wrap: wrap; font-size: 0.85rem; color: var(--mt-text-secondary);">
                <span>Audio Prep: <b>{metrics.get('audio', 0):.1f}s</b></span>
                <span>Whisper: <b>{metrics.get('whisper', 0):.1f}s</b></span>
                <span>Diarization: <b>{metrics.get('diarization', 0):.1f}s</b></span>
                <span>Alignment: <b>{metrics.get('alignment', 0):.1f}s</b></span>
                <span>AI Insights: <b>{metrics.get('llm', 0):.1f}s</b></span>
                <span>Total: <b style="color: var(--mt-primary);">{metrics.get('total', 0):.1f}s</b></span>
            </div>
        </div>
        ''', unsafe_allow_html=True)

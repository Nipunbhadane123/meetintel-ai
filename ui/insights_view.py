import streamlit as st
import json
import html
from ui.components import section_header, safe_escape, get_icon_svg, render_status_badge

def _safe_json_loads(val, default=None):
    if not val:
        return default if default is not None else []
    try:
        return json.loads(val)
    except Exception:
        return default if default is not None else []

def render_insights_tab(meeting):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        section_header("Overview & Strategic Insights", "AI-generated executive analysis of meeting dialogue, decisions, and outcomes.", category="Meeting Dossier")
    with col2:
        insights_data = {
            "executive_summary": meeting.executive_summary,
            "meeting_objective": meeting.meeting_objective,
            "emotional_analysis": meeting.emotional_analysis,
            "key_topics": _safe_json_loads(meeting.key_topics),
            "key_points": _safe_json_loads(meeting.key_points),
            "recommendations": _safe_json_loads(meeting.recommendations),
            "next_steps": _safe_json_loads(meeting.next_steps)
        }
        st.download_button("↓ Export (JSON)", data=json.dumps(insights_data, indent=2), file_name=f"Insights_{meeting.id}.json", mime="application/json", type="secondary", use_container_width=True)
        
    summary_text = safe_escape(meeting.executive_summary, default="No summary available.")
    
    # 1. Executive Summary
    with st.container(border=True):
        st.markdown(
            f"<div style='font-size: 0.72rem; font-weight: 700; color: var(--mt-primary); letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 4px;'>Executive Synthesis</div>"
            f"<h3 style='color: var(--mt-text); margin: 0 0 10px 0; font-size: 1.25rem; font-weight: 700;'>Executive Summary</h3>"
            f"<p style='color: var(--mt-text-secondary); font-size: 0.96rem; line-height: 1.7; margin: 0;'>{summary_text}</p>",
            unsafe_allow_html=True
        )
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 2. Objective & Emotional Analysis in a single unified container
    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            obj_text = safe_escape(meeting.meeting_objective, default="Not explicitly identified.")
            target_icon = get_icon_svg("target", size=18, color="#6C4DFF")
            st.markdown(f"<h4 style='color: var(--mt-text); margin: 0 0 6px 0; font-weight: 700; font-size: 1.05rem; display: flex; align-items: center; gap: 6px;'>{target_icon} Meeting Objective</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: var(--mt-text-secondary); line-height: 1.6; font-size: 0.9rem; margin: 0;'>{obj_text}</p>", unsafe_allow_html=True)
        with col_b:
            emo_text = safe_escape(meeting.emotional_analysis, default="Neutral")
            sparkle_icon = get_icon_svg("sparkles", size=18, color="#6C4DFF")
            st.markdown(f"<h4 style='color: var(--mt-text); margin: 0 0 6px 0; font-weight: 700; font-size: 1.05rem; display: flex; align-items: center; gap: 6px;'>{sparkle_icon} Emotional Tone & Engagement</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='color: var(--mt-text-secondary); line-height: 1.6; font-size: 0.9rem; margin: 0;'>{emo_text}</p>", unsafe_allow_html=True)
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 3. Two-column Detailed Breakdown with light dividers instead of nested bordered boxes
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 8px 0; font-weight: 700; font-size: 1.05rem;'>🔑 Key Topics</h4>", unsafe_allow_html=True)
            topics = _safe_json_loads(meeting.key_topics)
            if topics:
                for idx, t in enumerate(topics):
                    if idx > 0:
                        st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 6px 0;'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 0.88rem; color: var(--mt-text); padding: 2px 0;'>• {safe_escape(t)}</div>", unsafe_allow_html=True)
            else:
                st.caption("None recorded.")
                
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 8px 0; font-weight: 700; font-size: 1.05rem;'>💡 Key Discussion Points</h4>", unsafe_allow_html=True)
            points = _safe_json_loads(meeting.key_points)
            if points:
                for idx, p in enumerate(points):
                    if idx > 0:
                        st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 6px 0;'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 0.88rem; color: var(--mt-text); padding: 2px 0;'>• {safe_escape(p)}</div>", unsafe_allow_html=True)
            else:
                st.caption("None recorded.")
                
        with col2:
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 8px 0; font-weight: 700; font-size: 1.05rem;'>📌 Recommendations</h4>", unsafe_allow_html=True)
            recs = _safe_json_loads(meeting.recommendations)
            if recs:
                for idx, r in enumerate(recs):
                    if idx > 0:
                        st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 6px 0;'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 0.88rem; color: var(--mt-text); padding: 2px 0;'>• {safe_escape(r)}</div>", unsafe_allow_html=True)
            else:
                st.caption("None recorded.")
                
            st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 8px 0; font-weight: 700; font-size: 1.05rem;'>🚀 Next Steps</h4>", unsafe_allow_html=True)
            steps = _safe_json_loads(meeting.next_steps)
            if steps:
                for idx, s in enumerate(steps):
                    if idx > 0:
                        st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 6px 0;'></div>", unsafe_allow_html=True)
                    st.markdown(f"<div style='font-size: 0.88rem; color: var(--mt-text); padding: 2px 0;'>• {safe_escape(s)}</div>", unsafe_allow_html=True)
            else:
                st.caption("None recorded.")
        
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 4. Meeting Plan & Risks in a clean layout
    plan_text = safe_escape(meeting.meeting_plan, default="No specific follow-up plan registered.")
    with st.container(border=True):
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 6px 0; font-weight: 700; font-size: 1.05rem;'>📅 Meeting Plan & Follow-up</h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='color: var(--mt-text-secondary); line-height: 1.6; font-size: 0.9rem; margin: 0 0 14px 0;'>{plan_text}</p>", unsafe_allow_html=True)

        st.markdown("<div style='height: 1px; background: var(--mt-border); margin: 12px 0;'></div>", unsafe_allow_html=True)
        
        warn_icon = get_icon_svg("alert-triangle", size=18, color="#D98A16")
        st.markdown(f"<h4 style='color: var(--mt-warning); margin: 0 0 8px 0; font-weight: 700; font-size: 1.05rem; display: flex; align-items: center; gap: 6px;'>{warn_icon} Risks and Dependencies</h4>", unsafe_allow_html=True)
        risks = _safe_json_loads(meeting.risks)
        if risks:
            for risk in risks:
                if isinstance(risk, dict):
                    r_text = safe_escape(risk.get('risk', 'Unknown'))
                    imp = safe_escape(risk.get('impact', 'Unknown'))
                    ctx = safe_escape(risk.get('context', ''))
                    mit = safe_escape(risk.get('mitigation', ''))
                    st.markdown(f"<div style='padding: 4px 0; font-size: 0.88rem;'><strong>{r_text}</strong> <span style='color: var(--mt-text-secondary);'>(Impact: {imp})</span><br><span style='color: var(--mt-text-secondary);'>{ctx}</span></div>", unsafe_allow_html=True)
                    if mit:
                        st.markdown(f"<div style='color: var(--mt-primary); font-size: 0.84rem;'><em>Mitigation:</em> {mit}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='padding: 2px 0; font-size: 0.88rem; color: var(--mt-text);'>• {safe_escape(risk)}</div>", unsafe_allow_html=True)
        else:
            st.caption("No operational risks identified.")

    # Show performance metrics if available
    if 'last_metrics' in st.session_state:
        metrics = st.session_state['last_metrics']
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        with st.container(border=True):
            st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 10px 0; font-size: 0.95rem; font-weight: 600;'>⏱️ Processing Performance</h4>", unsafe_allow_html=True)
            col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
            with col_m1: st.caption("AUDIO PREP"); st.write(f"{metrics.get('audio', 0):.1f}s")
            with col_m2: st.caption("WHISPER"); st.write(f"{metrics.get('whisper', 0):.1f}s")
            with col_m3: st.caption("DIARIZATION"); st.write(f"{metrics.get('diarization', 0):.1f}s")
            with col_m4: st.caption("ALIGNMENT"); st.write(f"{metrics.get('alignment', 0):.1f}s")
            with col_m5: st.caption("AI INSIGHTS"); st.write(f"{metrics.get('llm', 0):.1f}s")
            with col_m6: st.caption("TOTAL"); st.markdown(f"<strong style='color: var(--mt-primary);'>{metrics.get('total', 0):.1f}s</strong>", unsafe_allow_html=True)

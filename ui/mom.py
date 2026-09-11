import streamlit as st
import json
import os
from pathlib import Path
from reports.pdf import generate_pdf
from reports.docx import generate_docx
from ui.components import section_header

REPORTS_DIR = Path("data/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_mom_text(meeting) -> str:
    lines = []
    lines.append("MINUTES OF MEETING")
    lines.append("=" * 20)
    lines.append(f"Title: {meeting.title}")
    lines.append(f"Date: {meeting.date.strftime('%Y-%m-%d %H:%M')}")
    duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s" if meeting.duration else "N/A"
    lines.append(f"Duration: {duration_str}")
    lines.append("")
    
    lines.append("1. EXECUTIVE SUMMARY")
    lines.append("-" * 20)
    lines.append(meeting.executive_summary if meeting.executive_summary else "N/A")
    lines.append("")
    
    lines.append("2. PARTICIPANTS")
    lines.append("-" * 20)
    if meeting.participants:
        for p in meeting.participants:
            lines.append(f"- {p.name} ({p.speaker_id})")
    else:
        lines.append("N/A")
    lines.append("")
    
    lines.append("3. KEY DISCUSSION POINTS")
    lines.append("-" * 20)
    key_points = json.loads(meeting.key_points) if meeting.key_points else []
    if key_points:
        for kp in key_points:
            lines.append(f"- {kp}")
    else:
        lines.append("N/A")
    lines.append("")
    
    lines.append("4. DECISIONS MADE")
    lines.append("-" * 20)
    if meeting.decisions:
        for d in meeting.decisions:
            lines.append(f"- {d.decision}")
    else:
        lines.append("N/A")
    lines.append("")
    
    lines.append("5. ACTION ITEMS & RESPONSIBILITIES")
    lines.append("-" * 20)
    if meeting.action_items:
        for ai in meeting.action_items:
            lines.append(f"- Task: {ai.task}")
            lines.append(f"  Assigned to: {ai.assigned_to}")
            lines.append(f"  Deadline: {ai.deadline}")
            lines.append(f"  Priority: {ai.priority}")
            lines.append(f"  Status: {ai.status}")
    else:
        lines.append("N/A")
    lines.append("")
    
    lines.append("6. RECOMMENDATIONS")
    lines.append("-" * 20)
    recs = json.loads(meeting.recommendations) if meeting.recommendations else []
    if recs:
        for r in recs:
            lines.append(f"- {r}")
    else:
        lines.append("N/A")
    lines.append("")
    
    return "\n".join(lines)


def render_mom_tab(meeting):
    section_header("📝 Minutes of Meeting", "Generated summary and exports")
    
    mom_text = generate_mom_text(meeting)
    
    with st.container():
        st.markdown(f"""
            <div class="mom-card-marker"></div>
            <style>
            div[data-testid="stVerticalBlock"]:has(.mom-card-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.mom-card-marker))) {{
                background: var(--surface) !important;
                border-radius: 20px !important;
                padding: 1.5rem !important;
                box-shadow: var(--shadow-soft) !important;
                border: 1px solid #E2E8F0 !important;
                margin-bottom: 2rem !important;
            }}
            .mom-card-marker {{ display: none; }}
            </style>
        """, unsafe_allow_html=True)
        st.text_area("MoM Preview", mom_text, height=400, label_visibility="collapsed")
    
    st.markdown("<h4 style='color: var(--text-main); margin-bottom: 1rem;'>↓ Export Options</h4>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="TXT Document",
            data=mom_text,
            file_name=f"MoM_{meeting.id}.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )
        
    with col2:
        pdf_path = REPORTS_DIR / f"MoM_{meeting.id}.pdf"
        if not pdf_path.exists() or True: # Regenerate for latest data
            generate_pdf(meeting, str(pdf_path))
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="PDF Document",
                data=f,
                file_name=f"MoM_{meeting.id}.pdf",
                mime="application/pdf",
                use_container_width=True,
                type="primary"
            )
            
    with col3:
        docx_path = REPORTS_DIR / f"MoM_{meeting.id}.docx"
        if not docx_path.exists() or True:
            generate_docx(meeting, str(docx_path))
        with open(docx_path, "rb") as f:
            st.download_button(
                label="Word Document",
                data=f,
                file_name=f"MoM_{meeting.id}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
                type="primary"
            )

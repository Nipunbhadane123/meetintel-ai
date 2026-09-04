import streamlit as st
import json
import os
from pathlib import Path
from reports.pdf import generate_pdf
from reports.docx import generate_docx

REPORTS_DIR = Path("data/reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_mom_text(meeting) -> str:
    lines = []
    lines.append("MINUTES OF MEETING")
    lines.append("=" * 20)
    lines.append(f"Title: {meeting.title}")
    lines.append(f"Date: {meeting.date.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Duration: {meeting.duration} seconds")
    lines.append("")
    
    lines.append("1. EXECUTIVE SUMMARY")
    lines.append("-" * 20)
    lines.append(meeting.executive_summary if meeting.executive_summary else "N/A")
    lines.append("")
    
    lines.append("2. MEETING OBJECTIVE")
    lines.append("-" * 20)
    lines.append(meeting.meeting_objective if meeting.meeting_objective else "N/A")
    lines.append("")
    
    lines.append("3. KEY TOPICS")
    lines.append("-" * 20)
    if meeting.key_topics:
        topics = json.loads(meeting.key_topics)
        for t in topics:
            lines.append(f"- {t}")
    else:
        lines.append("N/A")
    lines.append("")
    
    lines.append("4. ACTION ITEMS")
    lines.append("-" * 20)
    for ai in meeting.action_items:
        lines.append(f"- Task: {ai.task}")
        lines.append(f"  Owner: {ai.owner}")
        lines.append(f"  Deadline: {ai.deadline}")
        lines.append(f"  Status: {ai.status}")
    if not meeting.action_items:
        lines.append("N/A")
    lines.append("")
    
    lines.append("5. DECISIONS")
    lines.append("-" * 20)
    for d in meeting.decisions:
        lines.append(f"- {d.decision}")
        lines.append(f"  Context: {d.context}")
    if not meeting.decisions:
        lines.append("N/A")
    
    return "\n".join(lines)

def render_mom_tab(meeting):
    st.header("Minutes of Meeting")
    
    mom_text = generate_mom_text(meeting)
    
    st.text_area("MoM Preview", mom_text, height=400)
    
    st.markdown("### Export")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            label="Download TXT",
            data=mom_text,
            file_name=f"MoM_{meeting.title}.txt",
            mime="text/plain",
            use_container_width=True
        )
        
    with col2:
        pdf_path = REPORTS_DIR / f"MoM_{meeting.id}.pdf"
        if not pdf_path.exists():
            generate_pdf(meeting, str(pdf_path))
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name=f"MoM_{meeting.title}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
    with col3:
        docx_path = REPORTS_DIR / f"MoM_{meeting.id}.docx"
        if not docx_path.exists():
            generate_docx(meeting, str(docx_path))
        with open(docx_path, "rb") as f:
            st.download_button(
                label="Download DOCX",
                data=f,
                file_name=f"MoM_{meeting.title}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

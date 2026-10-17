import streamlit as st
import json
import os
from pathlib import Path
from reports.pdf import generate_pdf
from reports.docx import generate_docx
from ui.components import section_header, get_icon_svg

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
    try:
        key_points = json.loads(meeting.key_points) if meeting.key_points else []
    except Exception:
        key_points = []
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
    try:
        recs = json.loads(meeting.recommendations) if meeting.recommendations else []
    except Exception:
        recs = []
    if recs:
        for r in recs:
            lines.append(f"- {r}")
    else:
        lines.append("N/A")
    lines.append("")
    
    return "\n".join(lines)


def render_mom_tab(meeting):
    section_header("Minutes of Meeting (MoM)", "Consolidated executive summary, participants, decisions, and action items with multi-format export.", category="Meeting Dossier")
    
    mom_text = generate_mom_text(meeting)
    
    with st.container(border=True):
        st.caption("EXECUTIVE MINUTES OF MEETING (MOM) PREVIEW")
        st.text_area("MoM Preview", mom_text, height=420, label_visibility="collapsed")
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("<h4 style='color: var(--mt-text); margin: 0 0 12px 0; font-weight: 700; font-size: 1.05rem;'>↓ Multi-Format Report Exports</h4>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            pdf_path = REPORTS_DIR / f"MoM_{meeting.id}.pdf"
            if not pdf_path.exists():
                try:
                    generate_pdf(meeting, str(pdf_path))
                except Exception as e:
                    st.error(f"Failed to generate PDF: {e}")
                    
            if pdf_path.exists():
                try:
                    pdf_bytes = pdf_path.read_bytes()
                    st.download_button(
                        label="📄 Download PDF",
                        data=pdf_bytes,
                        file_name=f"MoM_{meeting.id}.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                        type="primary"
                    )
                except Exception:
                    st.error("Unable to prepare PDF.")
            else:
                st.button("PDF Unavailable", disabled=True, use_container_width=True)
                
        with col2:
            docx_path = REPORTS_DIR / f"MoM_{meeting.id}.docx"
            if not docx_path.exists():
                try:
                    generate_docx(meeting, str(docx_path))
                except Exception as e:
                    st.error(f"Failed to generate DOCX: {e}")
                    
            if docx_path.exists():
                try:
                    docx_bytes = docx_path.read_bytes()
                    st.download_button(
                        label="📝 Download Word",
                        data=docx_bytes,
                        file_name=f"MoM_{meeting.id}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True,
                        type="secondary"
                    )
                except Exception:
                    st.error("Unable to prepare DOCX.")
            else:
                st.button("Word Unavailable", disabled=True, use_container_width=True)

        with col3:
            try:
                from reports.csv import generate_csv
                csv_data = generate_csv(meeting)
                st.download_button(
                    label="📊 Download CSV",
                    data=csv_data.getvalue(),
                    file_name=f"MoM_{meeting.id}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    type="secondary"
                )
            except Exception:
                st.error("Unable to prepare CSV.")

        with col4:
            st.download_button(
                label="📃 Download TXT",
                data=mom_text,
                file_name=f"MoM_{meeting.id}.txt",
                mime="text/plain",
                use_container_width=True,
                type="secondary"
            )

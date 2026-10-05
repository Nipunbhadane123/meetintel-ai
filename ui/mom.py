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
                background: var(--mt-surface) !important;
                border-radius: var(--mt-radius-xl) !important;
                padding: var(--mt-space-xl) !important;
                box-shadow: var(--mt-shadow-soft) !important;
                border: 1px solid var(--mt-border) !important;
                margin-bottom: var(--mt-space-2xl) !important;
            }}
            div[data-testid="stVerticalBlock"]:has(.mom-card-marker) textarea {{
                font-family: 'Courier New', Courier, monospace !important;
                background: var(--mt-bg) !important;
                border: 1px solid var(--mt-border) !important;
                border-radius: var(--mt-radius-md) !important;
                padding: var(--mt-space-lg) !important;
                font-size: 0.95rem !important;
                line-height: 1.6 !important;
                color: var(--mt-text) !important;
                resize: none !important;
            }}
            .mom-card-marker {{ display: none; }}
            </style>
        """, unsafe_allow_html=True)
        st.text_area("MoM Preview", mom_text, height=450, label_visibility="collapsed")
    
    st.markdown("<h4 style='color: var(--mt-text); margin-bottom: var(--mt-space-lg); font-weight: 650; font-size: 1.25rem;'>↓ Export Options</h4>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.download_button(
            label="TXT",
            data=mom_text,
            file_name=f"MoM_{meeting.id}.txt",
            mime="text/plain",
            use_container_width=True,
            type="primary"
        )
        
    with col2:
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
                    label="PDF",
                    data=pdf_bytes,
                    file_name=f"MoM_{meeting.id}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error("Unable to prepare the PDF for download.")
            
    with col3:
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
                    label="Word",
                    data=docx_bytes,
                    file_name=f"MoM_{meeting.id}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True,
                    type="primary"
                )
            except Exception as e:
                st.error("Unable to prepare the DOCX for download.")

    with col4:
        try:
            from reports.csv import generate_csv
            csv_data = generate_csv(meeting)
            st.download_button(
                label="CSV",
                data=csv_data.getvalue(),
                file_name=f"MoM_{meeting.id}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary"
            )
        except Exception as e:
            st.error("Unable to prepare the CSV for download.")

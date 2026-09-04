from fpdf import FPDF
import json

class PDFReport(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 15)
        self.cell(0, 10, "MeetIntel AI - Minutes of Meeting", align="C")
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(meeting, output_path: str):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Title
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Meeting Title: {meeting.title}", ln=True)
    pdf.cell(0, 10, f"Date: {meeting.date.strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Duration: {meeting.duration} seconds", ln=True)
    pdf.ln(10)
    
    # Executive Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 7, meeting.executive_summary if meeting.executive_summary else "N/A")
    pdf.ln(5)
    
    # Action Items
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Action Items", ln=True)
    pdf.set_font("Helvetica", "", 10)
    if meeting.action_items:
        for ai in meeting.action_items:
            pdf.multi_cell(0, 7, f"- {ai.task} (Owner: {ai.owner}, Deadline: {ai.deadline}, Status: {ai.status})")
    else:
        pdf.multi_cell(0, 7, "None")
    pdf.ln(5)
    
    # Decisions
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Decisions", ln=True)
    pdf.set_font("Helvetica", "", 10)
    if meeting.decisions:
        for d in meeting.decisions:
            pdf.multi_cell(0, 7, f"- {d.decision} \n  Context: {d.context}")
    else:
        pdf.multi_cell(0, 7, "None")
    
    pdf.output(output_path)
    return output_path

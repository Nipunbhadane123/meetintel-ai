import os
from fpdf import FPDF
import json
import re

class PDFReport(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_font = "Helvetica"
            
    def header(self):
        self.set_font(self.default_font, "B", 15)
        self.cell(0, 10, "MeetIntel AI - Minutes of Meeting", align="C")
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font(self.default_font, "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def sanitize_text(self, text):
        if text is None:
            return "N/A"
        # FPDF standard fonts only support latin-1
        text = str(text)
        
        # Replace common unicode punctuation with closest ascii
        replacements = {
            '\u2018': "'", '\u2019': "'",
            '\u201c': '"', '\u201d': '"',
            '\u2013': "-", '\u2014': "-",
            '\u2026': "...",
            '\u2022': "-", # bullet
            '\u00a0': " ", # non-breaking space
            '\u2192': "->",
            '\u2190': "<-",
            '\t': '    '
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
            
        # Replace emojis and other non-latin-1 chars
        # fpdf2 allows passing error='replace' but let's be explicit
        return text.encode('latin-1', 'replace').decode('latin-1')

    def safe_multi_cell(self, w, h, txt, **kwargs):
        """Safely renders text by ensuring correct X position and wrapping extremely long words."""
        self.set_x(self.l_margin) # Force X to left margin
        
        txt = self.sanitize_text(txt)
        effective_w = self.epw if w == 0 else w
        if effective_w <= 0:
            effective_w = 100 # Safe fallback
            
        safe_lines = []
        for line in txt.split('\n'):
            words = line.split(' ')
            safe_line_words = []
            for word in words:
                # If word is very long, force break it
                while len(word) > 0 and self.get_string_width(word) > effective_w - 5:
                    for i in range(len(word), 0, -1):
                        if self.get_string_width(word[:i]) <= effective_w - 5:
                            safe_line_words.append(word[:i])
                            word = word[i:]
                            break
                    if not word: 
                        break
                if word:
                    safe_line_words.append(word)
            safe_lines.append(" ".join(safe_line_words))
            
        safe_txt = "\n".join(safe_lines)
        
        try:
            self.multi_cell(effective_w, h, safe_txt, **kwargs)
        except Exception as e:
            print(f"PDF rendering error on text snippet: {str(e)}")
            # Even this fails, try very basic output
            try:
                self.set_x(self.l_margin)
                self.cell(effective_w, h, "[Content error]")
                self.ln(h)
            except:
                pass

def generate_pdf(meeting, output_path: str):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    font = pdf.default_font
    
    pdf.set_font(font, "B", 12)
    pdf.safe_multi_cell(0, 10, f"Meeting Title: {meeting.title}")
    
    date_str = meeting.date.strftime('%Y-%m-%d %H:%M') if meeting.date else "Unknown"
    pdf.safe_multi_cell(0, 10, f"Date: {date_str}")
    
    duration_str = f"{int(meeting.duration)//60}m {int(meeting.duration)%60}s" if meeting.duration else "N/A"
    pdf.safe_multi_cell(0, 10, f"Duration: {duration_str}")
    pdf.ln(10)
    
    pdf.set_font(font, "B", 12)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.set_font(font, "", 10)
    pdf.safe_multi_cell(0, 7, meeting.executive_summary if meeting.executive_summary else "N/A")
    pdf.ln(5)
    
    pdf.set_font(font, "B", 12)
    pdf.cell(0, 10, "Participants", ln=True)
    pdf.set_font(font, "", 10)
    if meeting.participants:
        for p in meeting.participants:
            pdf.safe_multi_cell(0, 7, f"- {p.name} ({p.speaker_id})")
    else:
        pdf.safe_multi_cell(0, 7, "None")
    pdf.ln(5)
    
    pdf.set_font(font, "B", 12)
    pdf.cell(0, 10, "Action Items", ln=True)
    pdf.set_font(font, "", 10)
    if meeting.action_items:
        for ai in meeting.action_items:
            pdf.safe_multi_cell(0, 7, f"- {ai.task} (Assigned to: {ai.assigned_to}, Deadline: {ai.deadline}, Priority: {ai.priority})")
    else:
        pdf.safe_multi_cell(0, 7, "None")
    pdf.ln(5)
    
    pdf.set_font(font, "B", 12)
    pdf.cell(0, 10, "Decisions", ln=True)
    pdf.set_font(font, "", 10)
    if meeting.decisions:
        for d in meeting.decisions:
            pdf.safe_multi_cell(0, 7, f"- {d.decision}")
    else:
        pdf.safe_multi_cell(0, 7, "None")
        
    pdf.ln(10)
    pdf.set_font(font, "B", 12)
    pdf.cell(0, 10, "Transcript", ln=True)
    pdf.set_font(font, "", 9)
    if meeting.segments:
        for seg in meeting.segments:
            start_m = int(seg.start) // 60
            start_s = int(seg.start) % 60
            time_str = f"[{start_m:02d}:{start_s:02d}]"
            pdf.safe_multi_cell(0, 6, f"{time_str} {seg.speaker}: {seg.text}")
    else:
        pdf.safe_multi_cell(0, 7, "No transcript available.")
    
    pdf.output(output_path)
    return output_path

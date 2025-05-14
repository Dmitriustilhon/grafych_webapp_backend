from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER
import os

def generate_pdf(text: str, filename: str, title_info: dict = None) -> str:
    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    if title_info:
        title_style = ParagraphStyle(name="TitleStyle", parent=styles["Normal"], alignment=TA_CENTER, fontSize=16)
        story.append(Paragraph("Шпаргалка по инженерной графике", title_style))
        story.append(Spacer(1, 12))
        for key, value in title_info.items():
            story.append(Paragraph(f"{key.capitalize()}: {value}", styles["Normal"]))
        story.append(PageBreak())

    for line in text.split('\n'):
        if line.strip():
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 6))

    doc.build(story)
    return output_path

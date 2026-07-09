from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY


def build_offer_letter(placement, student, company):
    """Return a PDF (bytes) offer letter for a placement."""
    buf = BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            topMargin=2.2 * cm, bottomMargin=2 * cm,
                            leftMargin=2.2 * cm, rightMargin=2.2 * cm)
    styles = getSampleStyleSheet()

    title = ParagraphStyle('title', parent=styles['Title'], fontSize=20,
                           textColor=colors.HexColor('#4f46e5'), alignment=TA_CENTER, spaceAfter=6)
    sub = ParagraphStyle('sub', parent=styles['Normal'], fontSize=11,
                         textColor=colors.HexColor('#6b7280'), alignment=TA_CENTER, spaceAfter=20)
    body = ParagraphStyle('body', parent=styles['Normal'], fontSize=11, leading=18, alignment=TA_JUSTIFY, spaceAfter=12)

    name = f"{student.first_name} {student.last_name or ''}".strip()
    joining = placement.joining_date.strftime('%d %B %Y') if placement.joining_date else 'to be confirmed'
    today = datetime.utcnow().strftime('%d %B %Y')
    salary_txt = f"{placement.currency or 'INR'} {int(placement.salary):,}"

    story = [
        Paragraph(company.company_name, title),
        Paragraph("Offer of Employment", sub),
        Paragraph(f"Date: {today}", body),
        Paragraph(f"Dear {name},", body),
        Paragraph(
            f"We are pleased to offer you the position of <b>{placement.job_title}</b> at "
            f"{company.company_name}. After reviewing your application and interview performance, "
            f"we believe you will be a valuable addition to our team.", body),
        Paragraph(
            f"<b>Annual Compensation:</b> {salary_txt}<br/>"
            f"<b>Joining Date:</b> {joining}<br/>"
            + (f"<b>Bond Period:</b> {placement.bond_period} months<br/>" if placement.bond_period else "")
            + f"<b>Location:</b> {company.location or 'As per company policy'}", body),
        Paragraph(
            "This offer is subject to the verification of your documents and the terms and conditions "
            "of the company. We look forward to welcoming you aboard.", body),
        Spacer(1, 30),
        Paragraph("Warm regards,", body),
        Paragraph(f"<b>{company.company_name}</b><br/>Human Resources Department", body),
        Spacer(1, 20),
        Paragraph("This is a system-generated offer letter from the Placement Portal.",
                  ParagraphStyle('foot', parent=body, fontSize=8, textColor=colors.HexColor('#9ca3af'), alignment=TA_CENTER)),
    ]
    doc.build(story)
    buf.seek(0)
    return buf.read()

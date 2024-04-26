from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
import datetime

def create_pdf(data, title):
    title_style = getSampleStyleSheet()["Title"]
    title_paragraph = Paragraph(title, title_style)

    folder_path = "Reportes PDF"

    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    pdf_filename = os.path.join(folder_path, f"Resultados_de_escaneo_{timestamp}.pdf")
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)
    table = Table(data)

    table.setStyle(style)

    content = [title_paragraph, table]

    pdf.build(content)

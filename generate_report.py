import json
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def build_pdf():
    # Ensure the results file exists before trying to read it
    if not os.path.exists('audit_results.json'):
        print("Error: audit_results.json not found! Run auditor.py first.")
        input("\nPress Enter to exit...")
        return

    with open('audit_results.json', 'r') as f:
        data = json.load(f)

    doc = SimpleDocTemplate("Compliance_Gap_Analysis.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>Automated GRC Compliance & Gap Analysis Report</b>", styles['Title']))
    story.append(Spacer(1, 20))

    # Table Setup
    table_data = [["Control Framework ID", "Status", "Suggested Remediation Action"]]
    
    for item in data:
        status_color = f"<b><font color='green'>{item['status']}</font></b>" if item['status'] == "PASS" else f"<b><font color='red'>{item['status']}</font></b>"
        table_data.append([
            item['control'].replace('_', ' '),
            Paragraph(status_color, styles['Normal']),
            Paragraph(item['remediation'], styles['Normal'])
        ])

    # FIXED: Added explicit column widths [Width of Col 1, Col 2, Col 3] in points
    t = Table(table_data, colWidths=[180, 60, 250])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    story.append(t)
    doc.build(story)
    print("✨ Success! PDF Report generated: Compliance_Gap_Analysis.pdf")
    
    # Keeps the window open when double-clicking
    input("\nPress Enter to close this window...")

if __name__ == "__main__":
    build_pdf()
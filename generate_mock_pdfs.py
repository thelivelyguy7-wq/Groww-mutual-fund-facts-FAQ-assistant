from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import os

os.makedirs("mock_server", exist_ok=True)

schemes = [
    "HDFC Small Cap Fund",
    "HDFC Large Cap Fund",
    "HDFC Balanced Advantage Fund"
]

docs = ["Factsheet", "KIM", "SID", "FAQ", "Statement Guide"]

styles = getSampleStyleSheet()

data_lookup = {
    "HDFC Small Cap Fund": {"expense": "0.85%", "exit": "1% if redeemed within 1 year", "nav": "158.75", "min_sip": "Rs 500"},
    "HDFC Large Cap Fund": {"expense": "1.05%", "exit": "1% if redeemed within 1 year", "nav": "250.10", "min_sip": "Rs 100"},
    "HDFC Balanced Advantage Fund": {"expense": "0.90%", "exit": "1% if redeemed within 1 year", "nav": "310.45", "min_sip": "Rs 500"},
}

for scheme in schemes:
    for doc in docs:
        filename = f"mock_server/{scheme.replace(' ', '_')}_{doc.replace(' ', '_')}.pdf"
        pdf = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        elements.append(Paragraph(f"Official {doc}: {scheme}", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"This is the official {doc} document containing facts for {scheme}.", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        if doc in ["Factsheet", "KIM", "SID"]:
            data = [
                ["Metric", "Value"],
                ["Fund Name", scheme],
                ["Expense Ratio", data_lookup[scheme]["expense"]],
                ["Exit Load", data_lookup[scheme]["exit"]],
                ["Current NAV", data_lookup[scheme]["nav"]],
                ["Minimum SIP", data_lookup[scheme]["min_sip"]],
                ["Riskometer", "Very High"],
                ["Benchmark", "NIFTY 500"]
            ]
            
            t = Table(data)
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0,0), (-1,0), 12),
                ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ]))
            elements.append(t)
            
        elif doc == "FAQ":
            elements.append(Paragraph("Q: Can I invest via SIP?", styles['Heading2']))
            elements.append(Paragraph(f"A: Yes, the minimum SIP is {data_lookup[scheme]['min_sip']}.", styles['Normal']))
            
        elif doc == "Statement Guide":
            elements.append(Paragraph("How to download capital-gains statement", styles['Heading2']))
            elements.append(Paragraph("To download your capital gains statement, visit the HDFC Mutual Fund investor portal, login with your PAN, and navigate to 'Statements' -> 'Capital Gains'.", styles['Normal']))
            
        pdf.build(elements)
        print(f"Generated {filename}")

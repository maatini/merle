# scripts/generate_sample_pdfs.py
# Code comments in English.

import os
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_invoice_pdf(filename: Path, invoice_id: str, supplier: str, date: str, items: list[tuple[str, int, float]], vat_rate: float = 0.19) -> None:
    doc = SimpleDocTemplate(str(filename), pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'InvoiceTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1F4E79'),
        spaceAfter=20
    )
    meta_style = ParagraphStyle(
        'InvoiceMeta',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6
    )

    # Title & Header
    story.append(Paragraph(f"INVOICE", title_style))
    story.append(Spacer(1, 10))

    # Supplier & Metadata Details
    meta_data = [
        [Paragraph(f"<b>Supplier:</b> {supplier}", meta_style), Paragraph(f"<b>Invoice ID:</b> {invoice_id}", meta_style)],
        [Paragraph("<b>Address:</b> Business Park 4, Germany", meta_style), Paragraph(f"<b>Date:</b> {date}", meta_style)],
        [Paragraph("<b>Email:</b> accounting@supplier.com", meta_style), Paragraph("<b>Currency:</b> EUR", meta_style)]
    ]
    meta_table = Table(meta_data, colWidths=[250, 250])
    meta_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))

    # Items Table
    table_data = [['Description', 'Quantity', 'Unit Price', 'Total']]
    net_total = 0.0
    for desc, qty, price in items:
        item_total = qty * price
        net_total += item_total
        table_data.append([desc, str(qty), f"{price:.2f} EUR", f"{item_total:.2f} EUR"])

    vat_amount = net_total * vat_rate
    gross_total = net_total + vat_amount

    table_data.append(['', '', 'Net Total:', f"{net_total:.2f} EUR"])
    table_data.append(['', '', f"VAT ({int(vat_rate*100)}%):", f"{vat_amount:.2f} EUR"])
    table_data.append(['', '', 'Gross Total:', f"{gross_total:.2f} EUR"])

    items_table = Table(table_data, colWidths=[240, 60, 100, 100])
    items_table.setStyle(TableStyle([
        # Header style
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1F4E79')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        # Grid and alignments
        ('ALIGN', (1,1), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,len(items)), 0.5, colors.grey),
        ('LINEBELOW', (2,-3), (-1,-1), 1, colors.HexColor('#1F4E79')),
        ('FONTNAME', (2,-1), (-1,-1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,1), (-1,-1), 6),
    ]))
    story.append(items_table)

    # Build document
    doc.build(story)

def main() -> None:
    # Target directory: data/invoices inside examples/invoice-processing
    base_dir = Path(__file__).resolve().parent.parent
    output_dir = base_dir / "data" / "invoices"
    output_dir.mkdir(parents=True, exist_ok=True)

    invoices = [
        {
            "filename": output_dir / "INV-2025-0042.pdf",
            "invoice_id": "INV-2025-0042",
            "supplier": "ACME GmbH",
            "date": "2025-05-10",
            "items": [("Consulting services", 10, 1245.00)]
        },
        {
            "filename": output_dir / "INV-2025-0043.pdf",
            "invoice_id": "INV-2025-0043",
            "supplier": "Globex AG",
            "date": "2025-05-11",
            "items": [
                ("Hardware components", 5, 150.00),
                ("Shipping & Handling", 1, 125.50)
            ]
        },
        {
            "filename": output_dir / "INV-2025-0044.pdf",
            "invoice_id": "INV-2025-0044",
            "supplier": "Initech Ltd.",
            "date": "2025-05-12",
            "items": [("Software license renewal", 2, 1170.00)]
        }
    ]

    for inv in invoices:
        create_invoice_pdf(**inv)
        print(f"Generated sample PDF invoice: {inv['filename'].name}")

if __name__ == "__main__":
    main()

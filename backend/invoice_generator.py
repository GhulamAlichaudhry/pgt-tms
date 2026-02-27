"""
Invoice Generator Service
Professional invoice generation with company branding
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from io import BytesIO
from typing import Optional, Dict, List
import os

class InvoiceGenerator:
    def __init__(self):
        self.company_info = {
            "name": "PGT International (Private) Limited",
            "tagline": "Excellence in Transportation & Logistics",
            "address": "Main Office Address, City, Country",
            "phone": "+92-XXX-XXXXXXX",
            "email": "info@pgtinternational.com",
            "website": "www.pgtinternational.com",
            "tax_id": "NTN: XXXXXXX-X"
        }
    
    def generate_invoice_pdf(
        self,
        invoice_data: Dict,
        client_data: Dict,
        items: List[Dict],
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate professional invoice PDF
        
        invoice_data: {
            'invoice_number': 'INV-2026-001',
            'invoice_date': '2026-02-27',
            'due_date': '2026-03-29',
            'reference': 'Trip #123',
            'notes': 'Thank you for your business'
        }
        
        client_data: {
            'name': 'ABC Company',
            'contact_person': 'John Doe',
            'address': 'Client Address',
            'phone': '+92-XXX-XXXXXXX',
            'email': 'client@example.com'
        }
        
        items: [
            {
                'description': 'Transportation Service',
                'quantity': 1,
                'rate': 50000,
                'amount': 50000
            }
        ]
        """
        buffer = BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(
            buffer if not output_path else output_path,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        # Container for elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#374151'),
            spaceAfter=12,
            fontName='Helvetica-Bold'
        )
        
        # Company Header
        elements.append(Paragraph(self.company_info['name'], title_style))
        elements.append(Paragraph(self.company_info['tagline'], subtitle_style))
        elements.append(Spacer(1, 0.1*inch))
        
        # Company Info
        company_info_text = f"""
        <font size=9 color="#374151">
        {self.company_info['address']}<br/>
        Phone: {self.company_info['phone']} | Email: {self.company_info['email']}<br/>
        Website: {self.company_info['website']} | {self.company_info['tax_id']}
        </font>
        """
        elements.append(Paragraph(company_info_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Invoice Title
        invoice_title = f'<font size=18 color="#dc2626"><b>INVOICE</b></font>'
        elements.append(Paragraph(invoice_title, ParagraphStyle('InvoiceTitle', alignment=TA_CENTER)))
        elements.append(Spacer(1, 0.2*inch))
        
        # Invoice Details and Client Info (Side by side)
        invoice_client_data = [
            ['Invoice Details', 'Bill To'],
            [
                f"Invoice #: {invoice_data['invoice_number']}\n"
                f"Date: {invoice_data['invoice_date']}\n"
                f"Due Date: {invoice_data['due_date']}\n"
                f"Reference: {invoice_data.get('reference', 'N/A')}",
                
                f"{client_data['name']}\n"
                f"Attn: {client_data.get('contact_person', 'N/A')}\n"
                f"{client_data.get('address', 'N/A')}\n"
                f"Phone: {client_data.get('phone', 'N/A')}\n"
                f"Email: {client_data.get('email', 'N/A')}"
            ]
        ]
        
        invoice_client_table = Table(invoice_client_data, colWidths=[3.5*inch, 3.5*inch])
        invoice_client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 1), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        elements.append(invoice_client_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Items Table
        items_data = [['Description', 'Quantity', 'Rate (PKR)', 'Amount (PKR)']]
        
        subtotal = 0
        for item in items:
            items_data.append([
                item['description'],
                str(item.get('quantity', 1)),
                f"{item['rate']:,.2f}",
                f"{item['amount']:,.2f}"
            ])
            subtotal += item['amount']
        
        items_table = Table(items_data, colWidths=[3.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
        ]))
        elements.append(items_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Totals
        tax_rate = invoice_data.get('tax_rate', 0)
        tax_amount = subtotal * (tax_rate / 100) if tax_rate > 0 else 0
        total = subtotal + tax_amount
        
        totals_data = []
        totals_data.append(['', '', 'Subtotal:', f"PKR {subtotal:,.2f}"])
        
        if tax_rate > 0:
            totals_data.append(['', '', f'Tax ({tax_rate}%):', f"PKR {tax_amount:,.2f}"])
        
        totals_data.append(['', '', 'Total Amount:', f"PKR {total:,.2f}"])
        
        totals_table = Table(totals_data, colWidths=[3.5*inch, 1*inch, 1.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (2, 0), (2, -2), 'Helvetica'),
            ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (2, 0), (-1, -2), 10),
            ('FONTSIZE', (2, -1), (-1, -1), 12),
            ('TEXTCOLOR', (2, 0), (-1, -2), colors.HexColor('#374151')),
            ('TEXTCOLOR', (2, -1), (-1, -1), colors.HexColor('#dc2626')),
            ('LINEABOVE', (2, -1), (-1, -1), 2, colors.HexColor('#dc2626')),
            ('TOPPADDING', (2, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (2, 0), (-1, -1), 6),
            ('RIGHTPADDING', (2, 0), (-1, -1), 12)
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Payment Terms
        if invoice_data.get('payment_terms'):
            elements.append(Paragraph('<b>Payment Terms:</b>', heading_style))
            elements.append(Paragraph(invoice_data['payment_terms'], styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Notes
        if invoice_data.get('notes'):
            elements.append(Paragraph('<b>Notes:</b>', heading_style))
            elements.append(Paragraph(invoice_data['notes'], styles['Normal']))
            elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        elements.append(Spacer(1, 0.3*inch))
        footer_text = """
        <font size=8 color="#6b7280">
        <b>Thank you for your business!</b><br/>
        For any queries regarding this invoice, please contact our accounts department.<br/>
        This is a computer-generated invoice and does not require a signature.
        </font>
        """
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(elements)
        
        if not output_path:
            buffer.seek(0)
            return buffer
        
        return None
    
    def generate_invoice_number(self, db_session) -> str:
        """Generate next invoice number"""
        from datetime import datetime
        import models
        
        # Get current year and month
        now = datetime.now()
        year = now.year
        month = now.strftime('%m')
        
        # Count invoices this month
        prefix = f"INV-{year}{month}"
        count = db_session.query(models.Receivable).filter(
            models.Receivable.invoice_number.like(f"{prefix}%")
        ).count()
        
        # Generate new number
        next_num = count + 1
        return f"{prefix}-{next_num:04d}"

# Singleton instance
invoice_generator = InvoiceGenerator()

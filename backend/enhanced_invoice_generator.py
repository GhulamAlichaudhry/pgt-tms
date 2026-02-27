"""
Enhanced Invoice Generator Service
Modern, elegant, professional invoice generation with complete trip details
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from datetime import datetime
from io import BytesIO
from typing import Optional, Dict, List
import os
from pathlib import Path

class EnhancedInvoiceGenerator:
    def __init__(self):
        self.company_info = {
            "name": "PGT INTERNATIONAL (PVT) LTD",
            "tagline": "Excellence in Transportation & Logistics",
            "address": "Office # 7, 1st Floor, Haji Yousuf Plaza, Near Memon Masjid, M.A Jinnah Road, Karachi",
            "phone": "+92-21-32412345",
            "mobile": "+92-300-1234567",
            "email": "info@pgtinternational.com",
            "website": "www.pgtinternational.com",
            "ntn": "NTN: 1234567-8",
            "bank_details": {
                "bank_name": "Meezan Bank Limited",
                "branch": "M.A. Jinnah Road Branch",
                "account_title": "PGT International (Pvt) Ltd",
                "account_number": "01234567890123",
                "iban": "PK12 MEZN 0001 2345 6789 0123"
            }
        }
        
        # Logo path (if exists)
        self.logo_path = Path("backend/static/logo.png")
        if not self.logo_path.exists():
            self.logo_path = None
    
    def generate_detailed_invoice_pdf(
        self,
        invoice_data: Dict,
        client_data: Dict,
        trip_data: Dict,
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate modern, elegant, one-page invoice PDF
        """
        buffer = BytesIO()
        
        # Create PDF with tighter margins for one-page fit
        doc = SimpleDocTemplate(
            buffer if not output_path else output_path,
            pagesize=letter,
            rightMargin=0.4*inch,
            leftMargin=0.4*inch,
            topMargin=0.3*inch,
            bottomMargin=0.3*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # ============================================
        # MODERN HEADER WITH LOGO
        # ============================================
        
        # Create header table with logo and company info
        header_data = []
        
        if self.logo_path and self.logo_path.exists():
            # With logo
            logo = Image(str(self.logo_path), width=1.2*inch, height=1.2*inch)
            company_info_text = f"""
            <font size=16 color="#1e40af"><b>{self.company_info['name']}</b></font><br/>
            <font size=8 color="#64748b"><i>{self.company_info['tagline']}</i></font>
            """
            header_data = [[logo, Paragraph(company_info_text, styles['Normal'])]]
            header_table = Table(header_data, colWidths=[1.5*inch, 5.5*inch])
            header_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
        else:
            # Without logo - just company name
            company_header = f"""
            <font size=18 color="#1e40af"><b>{self.company_info['name']}</b></font><br/>
            <font size=9 color="#64748b"><i>{self.company_info['tagline']}</i></font>
            """
            header_table = Paragraph(company_header, ParagraphStyle('CompanyHeader', alignment=TA_CENTER))
        
        elements.append(header_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # Contact details in compact format
        contact_details = f"""
        <font size=7 color="#475569">
        <b>Address:</b> {self.company_info['address']}<br/>
        <b>Phone:</b> {self.company_info['phone']} | <b>Mobile:</b> {self.company_info['mobile']} | 
        <b>Email:</b> {self.company_info['email']} | <b>Web:</b> {self.company_info['website']}<br/>
        <b>{self.company_info['ntn']}</b>
        </font>
        """
        elements.append(Paragraph(contact_details, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Decorative line
        line_table = Table([['']], colWidths=[7.2*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#1e40af')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # ============================================
        # INVOICE TITLE & INFO SECTION (COMPACT)
        # ============================================
        
        invoice_header_data = [
            [
                Paragraph('<font size=16 color="#1e40af"><b>TRANSPORTATION INVOICE</b></font>', 
                         ParagraphStyle('InvTitle', alignment=TA_LEFT)),
                Paragraph(f'<font size=10 color="#1e40af"><b>Invoice #: {invoice_data["invoice_number"]}</b></font><br/>'
                         f'<font size=8 color="#64748b">Date: {invoice_data["invoice_date"]}<br/>'
                         f'Due: {invoice_data["due_date"]}</font>', 
                         ParagraphStyle('InvInfo', alignment=TA_RIGHT))
            ]
        ]
        
        invoice_header_table = Table(invoice_header_data, colWidths=[4*inch, 3.2*inch])
        invoice_header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(invoice_header_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # CLIENT & TRIP INFO (SIDE BY SIDE - COMPACT)
        # ============================================
        
        client_trip_data = [
            [
                Paragraph('<font size=9 color="#1e40af"><b>BILL TO</b></font>', styles['Normal']),
                Paragraph('<font size=9 color="#1e40af"><b>TRIP DETAILS</b></font>', styles['Normal'])
            ],
            [
                Paragraph(f"""
                <font size=8>
                <b>{client_data['name']}</b><br/>
                {client_data.get('contact_person', 'N/A')}<br/>
                {client_data.get('address', 'N/A')}<br/>
                <b>Phone:</b> {client_data.get('phone', 'N/A')}<br/>
                <b>Email:</b> {client_data.get('email', 'N/A')}
                </font>
                """, styles['Normal']),
                
                Paragraph(f"""
                <font size=8>
                <b>Ref:</b> {trip_data.get('reference_no', 'N/A')} | <b>Date:</b> {trip_data.get('date', 'N/A')}<br/>
                <b>Vehicle:</b> {trip_data.get('vehicle_number', 'N/A')} | <b>Driver:</b> {trip_data.get('driver_name', 'N/A')}<br/>
                <b>From:</b> {trip_data.get('source_location', 'N/A')} <b>To:</b> {trip_data.get('destination_location', 'N/A')}<br/>
                <b>Cargo:</b> {trip_data.get('category_product', 'N/A')} | <b>Weight:</b> {trip_data.get('total_tonnage', 0):.2f} MT
                </font>
                """, styles['Normal'])
            ]
        ]
        
        client_trip_table = Table(client_trip_data, colWidths=[3.6*inch, 3.6*inch])
        client_trip_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eff6ff')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(client_trip_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # CHARGES TABLE (MODERN DESIGN)
        # ============================================
        
        charges_data = [
            [
                Paragraph('<font size=9 color="white"><b>DESCRIPTION</b></font>', styles['Normal']),
                Paragraph('<font size=9 color="white"><b>QTY</b></font>', ParagraphStyle('Center', alignment=TA_CENTER)),
                Paragraph('<font size=9 color="white"><b>RATE</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph('<font size=9 color="white"><b>AMOUNT</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ]
        ]
        
        # Service description
        service_desc = f"Transportation Service\n{trip_data.get('source_location', '')} → {trip_data.get('destination_location', '')}"
        if trip_data.get('category_product'):
            service_desc += f"\n{trip_data.get('category_product')}"
        
        if trip_data.get('freight_mode') == 'per_ton':
            qty_text = f"{trip_data.get('tonnage', trip_data.get('total_tonnage', 0)):.2f} MT"
            rate_text = f"PKR {trip_data.get('rate_per_ton', 0):,.2f}"
        else:
            qty_text = "1"
            rate_text = f"PKR {trip_data.get('client_freight', 0):,.2f}"
        
        amount = trip_data.get('client_freight', 0)
        
        charges_data.append([
            Paragraph(f'<font size=8>{service_desc}</font>', styles['Normal']),
            Paragraph(f'<font size=8>{qty_text}</font>', ParagraphStyle('Center', alignment=TA_CENTER)),
            Paragraph(f'<font size=8>{rate_text}</font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
            Paragraph(f'<font size=8><b>PKR {amount:,.2f}</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
        ])
        
        charges_table = Table(charges_data, colWidths=[3.8*inch, 1*inch, 1.2*inch, 1.2*inch])
        charges_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e40af')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
        ]))
        elements.append(charges_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # ============================================
        # TOTALS (MODERN DESIGN)
        # ============================================
        
        subtotal = trip_data.get('client_freight', 0)
        tax_amount = invoice_data.get('tax_amount', 0)
        discount_amount = invoice_data.get('discount_amount', 0)
        total_amount = subtotal + tax_amount - discount_amount
        
        totals_data = [
            ['', '', Paragraph('<font size=9><b>Subtotal:</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)), 
             Paragraph(f'<font size=9>PKR {subtotal:,.2f}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))],
        ]
        
        if tax_amount > 0:
            totals_data.append([
                '', '', Paragraph('<font size=9><b>Tax:</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph(f'<font size=9>PKR {tax_amount:,.2f}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ])
        
        if discount_amount > 0:
            totals_data.append([
                '', '', Paragraph('<font size=9><b>Discount:</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph(f'<font size=9>- PKR {discount_amount:,.2f}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ])
        
        totals_data.append([
            '', '', 
            Paragraph('<font size=11 color="#1e40af"><b>TOTAL AMOUNT:</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
            Paragraph(f'<font size=11 color="#1e40af"><b>PKR {total_amount:,.2f}</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
        ])
        
        totals_table = Table(totals_data, colWidths=[3.8*inch, 1*inch, 1.2*inch, 1.2*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEABOVE', (2, -1), (-1, -1), 2, colors.HexColor('#1e40af')),
            ('BACKGROUND', (2, -1), (-1, -1), colors.HexColor('#eff6ff')),
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # PAYMENT INFO & BANK DETAILS (COMPACT)
        # ============================================
        
        payment_bank_data = [
            [
                Paragraph('<font size=8 color="#1e40af"><b>PAYMENT TERMS</b></font>', styles['Normal']),
                Paragraph('<font size=8 color="#1e40af"><b>BANK DETAILS</b></font>', styles['Normal'])
            ],
            [
                Paragraph(f"""
                <font size=7>
                {invoice_data.get('payment_terms', 'Payment due within 30 days')}<br/>
                <b>Due Date:</b> {invoice_data['due_date']}
                </font>
                """, styles['Normal']),
                
                Paragraph(f"""
                <font size=7>
                <b>Bank:</b> {self.company_info['bank_details']['bank_name']}<br/>
                <b>Branch:</b> {self.company_info['bank_details']['branch']}<br/>
                <b>Account:</b> {self.company_info['bank_details']['account_title']}<br/>
                <b>A/C #:</b> {self.company_info['bank_details']['account_number']}<br/>
                <b>IBAN:</b> {self.company_info['bank_details']['iban']}
                </font>
                """, styles['Normal'])
            ]
        ]
        
        payment_bank_table = Table(payment_bank_data, colWidths=[3.6*inch, 3.6*inch])
        payment_bank_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#eff6ff')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(payment_bank_table)
        elements.append(Spacer(1, 0.1*inch))
        
        # ============================================
        # NOTES (IF ANY)
        # ============================================
        
        if invoice_data.get('notes'):
            notes_text = f'<font size=7 color="#64748b"><b>Notes:</b> {invoice_data["notes"]}</font>'
            elements.append(Paragraph(notes_text, styles['Normal']))
            elements.append(Spacer(1, 0.08*inch))
        
        # ============================================
        # FOOTER (COMPACT)
        # ============================================
        
        footer_line = Table([['']], colWidths=[7.2*inch])
        footer_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#cbd5e1')),
        ]))
        elements.append(footer_line)
        elements.append(Spacer(1, 0.05*inch))
        
        footer_text = f"""
        <font size=7 color="#64748b">
        <b>Thank you for your business!</b> | 
        For queries: {self.company_info['phone']} or {self.company_info['email']} | 
        Generated: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}
        </font>
        """
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(elements)
        
        if not output_path:
            buffer.seek(0)
            return buffer
        return None
        """
        Generate professional invoice PDF with complete trip details
        
        invoice_data: {
            'invoice_number': 'INV-2026-001',
            'invoice_date': '2026-02-27',
            'due_date': '2026-03-29',
            'payment_terms': 'Payment due within 30 days',
            'notes': 'Thank you for your business'
        }
        
        client_data: {
            'name': 'ABC Company',
            'contact_person': 'John Doe',
            'address': 'Client Address',
            'phone': '+92-XXX-XXXXXXX',
            'email': 'client@example.com'
        }
        
        trip_data: {
            'reference_no': 'TRP-2026-001',
            'date': '2026-02-27',
            'vehicle_number': 'ABC-123',
            'driver_name': 'Driver Name',
            'source_location': 'Karachi',
            'destination_location': 'Lahore',
            'category_product': 'General Cargo',
            'total_tonnage': 25.5,
            'freight_mode': 'per_ton',
            'rate_per_ton': 2000,
            'client_freight': 51000,
            'description': 'Transportation service details'
        }
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
            fontSize=26,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=4,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=8,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        
        # ============================================
        # COMPANY HEADER
        # ============================================
        elements.append(Paragraph(self.company_info['name'], title_style))
        elements.append(Paragraph(self.company_info['tagline'], subtitle_style))
        
        # Company contact info
        company_info_text = f"""
        <font size=8 color="#374151">
        {self.company_info['address']}<br/>
        Phone: {self.company_info['phone']} | Email: {self.company_info['email']} | Web: {self.company_info['website']}<br/>
        {self.company_info['tax_id']}
        </font>
        """
        elements.append(Paragraph(company_info_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Horizontal line
        line_table = Table([['']], colWidths=[7*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#dc2626')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # INVOICE TITLE
        # ============================================
        invoice_title = '<font size=20 color="#dc2626"><b>TRANSPORTATION INVOICE</b></font>'
        elements.append(Paragraph(invoice_title, ParagraphStyle('InvoiceTitle', alignment=TA_CENTER)))
        elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # INVOICE & CLIENT INFO (Side by Side)
        # ============================================
        invoice_client_data = [
            [
                Paragraph('<b><font size=11 color="#dc2626">Invoice Details</font></b>', styles['Normal']),
                Paragraph('<b><font size=11 color="#dc2626">Bill To</font></b>', styles['Normal'])
            ],
            [
                Paragraph(f"""
                <font size=9>
                <b>Invoice #:</b> {invoice_data['invoice_number']}<br/>
                <b>Invoice Date:</b> {invoice_data['invoice_date']}<br/>
                <b>Due Date:</b> {invoice_data['due_date']}<br/>
                <b>Trip Reference:</b> {trip_data.get('reference_no', 'N/A')}
                </font>
                """, styles['Normal']),
                
                Paragraph(f"""
                <font size=9>
                <b>{client_data['name']}</b><br/>
                Attn: {client_data.get('contact_person', 'N/A')}<br/>
                {client_data.get('address', 'N/A')}<br/>
                Phone: {client_data.get('phone', 'N/A')}<br/>
                Email: {client_data.get('email', 'N/A')}
                </font>
                """, styles['Normal'])
            ]
        ]
        
        invoice_client_table = Table(invoice_client_data, colWidths=[3.5*inch, 3.5*inch])
        invoice_client_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#d1d5db')),
        ]))
        elements.append(invoice_client_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # ============================================
        # TRIP DETAILS (Prominent - Like Manual Invoice)
        # ============================================
        elements.append(Paragraph('<b><font size=12 color="#dc2626">Trip Details</font></b>', styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        trip_details_data = [
            ['Trip Date:', trip_data.get('date', 'N/A'), 'Vehicle Number:', trip_data.get('vehicle_number', 'N/A')],
            ['Driver/Operator:', trip_data.get('driver_name', 'N/A'), 'Cargo Type:', trip_data.get('category_product', 'N/A')],
            ['From (Origin):', trip_data.get('source_location', 'N/A'), 'To (Destination):', trip_data.get('destination_location', 'N/A')],
            ['Total Tonnage:', f"{trip_data.get('total_tonnage', 0):.2f} MT", 'Freight Mode:', trip_data.get('freight_mode', 'total').upper()],
        ]
        
        # Add rate per ton if applicable
        if trip_data.get('freight_mode') == 'per_ton' and trip_data.get('rate_per_ton'):
            trip_details_data.append([
                'Rate per Ton:', 
                f"PKR {trip_data.get('rate_per_ton', 0):,.2f}", 
                'Tonnage for Billing:', 
                f"{trip_data.get('tonnage', trip_data.get('total_tonnage', 0)):.2f} MT"
            ])
        
        trip_details_table = Table(trip_details_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        trip_details_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f9fafb')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#f9fafb')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(trip_details_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # ============================================
        # CHARGES BREAKDOWN
        # ============================================
        elements.append(Paragraph('<b><font size=12 color="#dc2626">Charges</font></b>', styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Prepare charges data
        charges_data = [
            ['Description', 'Quantity', 'Rate', 'Amount']
        ]
        
        # Main freight charge
        if trip_data.get('freight_mode') == 'per_ton':
            charges_data.append([
                f"Transportation Service\n{trip_data.get('source_location', '')} to {trip_data.get('destination_location', '')}\n{trip_data.get('category_product', '')}",
                f"{trip_data.get('tonnage', trip_data.get('total_tonnage', 0)):.2f} MT",
                f"PKR {trip_data.get('rate_per_ton', 0):,.2f}",
                f"PKR {trip_data.get('client_freight', 0):,.2f}"
            ])
        else:
            charges_data.append([
                f"Transportation Service\n{trip_data.get('source_location', '')} to {trip_data.get('destination_location', '')}\n{trip_data.get('category_product', '')}",
                "1",
                f"PKR {trip_data.get('client_freight', 0):,.2f}",
                f"PKR {trip_data.get('client_freight', 0):,.2f}"
            ])
        
        # Calculate totals
        subtotal = trip_data.get('client_freight', 0)
        tax_amount = invoice_data.get('tax_amount', 0)
        discount_amount = invoice_data.get('discount_amount', 0)
        total_amount = subtotal + tax_amount - discount_amount
        
        charges_table = Table(charges_data, colWidths=[3.5*inch, 1*inch, 1.25*inch, 1.25*inch])
        charges_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#d1d5db')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(charges_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # TOTALS SECTION
        # ============================================
        totals_data = [
            ['Subtotal:', f"PKR {subtotal:,.2f}"],
        ]
        
        if tax_amount > 0:
            totals_data.append(['Tax:', f"PKR {tax_amount:,.2f}"])
        
        if discount_amount > 0:
            totals_data.append(['Discount:', f"- PKR {discount_amount:,.2f}"])
        
        totals_data.append(['', ''])  # Spacer
        totals_data.append(['TOTAL AMOUNT DUE:', f"PKR {total_amount:,.2f}"])
        
        totals_table = Table(totals_data, colWidths=[5.5*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -2), 10),
            ('FONTSIZE', (0, -1), (-1, -1), 12),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fee2e2')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.HexColor('#dc2626')),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#dc2626')),
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # ============================================
        # PAYMENT TERMS & BANK DETAILS
        # ============================================
        elements.append(Paragraph('<b><font size=11 color="#dc2626">Payment Information</font></b>', styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        payment_info_data = [
            [
                Paragraph(f"""
                <font size=9>
                <b>Payment Terms:</b><br/>
                {invoice_data.get('payment_terms', 'Payment due within 30 days')}<br/>
                <br/>
                <b>Due Date:</b> {invoice_data['due_date']}
                </font>
                """, styles['Normal']),
                
                Paragraph(f"""
                <font size=9>
                <b>Bank Details:</b><br/>
                Bank: {self.company_info['bank_details']['bank_name']}<br/>
                Account Title: {self.company_info['bank_details']['account_title']}<br/>
                Account #: {self.company_info['bank_details']['account_number']}<br/>
                IBAN: {self.company_info['bank_details']['iban']}
                </font>
                """, styles['Normal'])
            ]
        ]
        
        payment_info_table = Table(payment_info_data, colWidths=[3.5*inch, 3.5*inch])
        payment_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#d1d5db')),
        ]))
        elements.append(payment_info_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # NOTES & TERMS
        # ============================================
        if invoice_data.get('notes'):
            elements.append(Paragraph('<b><font size=10 color="#374151">Notes:</font></b>', styles['Normal']))
            elements.append(Spacer(1, 0.05*inch))
            notes_text = f'<font size=9 color="#6b7280">{invoice_data["notes"]}</font>'
            elements.append(Paragraph(notes_text, styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # FOOTER
        # ============================================
        elements.append(Spacer(1, 0.2*inch))
        footer_line = Table([['']], colWidths=[7*inch])
        footer_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#d1d5db')),
        ]))
        elements.append(footer_line)
        elements.append(Spacer(1, 0.1*inch))
        
        footer_text = f"""
        <font size=8 color="#6b7280">
        <b>Thank you for your business!</b><br/>
        This is a computer-generated invoice. For any queries, please contact us at {self.company_info['phone']} or {self.company_info['email']}<br/>
        Generated on: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
        </font>
        """
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(elements)
        
        if not output_path:
            buffer.seek(0)
            return buffer
        return None
    
    def generate_invoice_from_trip_id(self, db, trip_id: int) -> BytesIO:
        """
        Generate invoice directly from trip ID
        Fetches all required data from database
        """
        import models
        from datetime import timedelta
        
        # Get trip
        trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
        if not trip:
            raise ValueError(f"Trip {trip_id} not found")
        
        # Get receivable
        receivable = db.query(models.Receivable).filter(
            models.Receivable.trip_id == trip_id
        ).first()
        
        if not receivable:
            raise ValueError(f"No receivable found for trip {trip_id}")
        
        # Prepare invoice data
        invoice_data = {
            'invoice_number': receivable.invoice_number,
            'invoice_date': receivable.invoice_date.strftime('%Y-%m-%d'),
            'due_date': receivable.due_date.strftime('%Y-%m-%d'),
            'payment_terms': f'Payment due within {receivable.payment_terms} days',
            'notes': 'Thank you for your business! Please make payment by the due date.',
            'tax_amount': 0,
            'discount_amount': 0
        }
        
        # Prepare client data
        client = trip.client
        client_data = {
            'name': client.name,
            'contact_person': client.contact_person or 'N/A',
            'address': client.address or 'N/A',
            'phone': client.phone or 'N/A',
            'email': client.email or 'N/A'
        }
        
        # Prepare trip data
        trip_data = {
            'reference_no': trip.reference_no,
            'date': trip.date.strftime('%Y-%m-%d') if trip.date else 'N/A',
            'vehicle_number': trip.vehicle.vehicle_no if trip.vehicle else 'N/A',
            'driver_name': trip.driver_operator or 'N/A',
            'source_location': trip.source_location,
            'destination_location': trip.destination_location,
            'category_product': trip.category_product,
            'total_tonnage': float(trip.total_tonnage),
            'freight_mode': trip.freight_mode,
            'rate_per_ton': float(trip.rate_per_ton) if trip.rate_per_ton else 0,
            'tonnage': float(trip.tonnage) if trip.tonnage else float(trip.total_tonnage),
            'client_freight': float(trip.client_freight),
            'description': receivable.description
        }
        
        # Generate PDF
        return self.generate_detailed_invoice_pdf(
            invoice_data=invoice_data,
            client_data=client_data,
            trip_data=trip_data
        )


# Create singleton instance
enhanced_invoice_generator = EnhancedInvoiceGenerator()

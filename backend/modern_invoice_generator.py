"""
Modern Commercial Invoice Generator
Professional branding with Theme A (Blue) and Theme B (Red/Black)
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
from datetime import datetime
from io import BytesIO
from typing import Optional, Dict
import os
from pathlib import Path
import qrcode

class ModernInvoiceGenerator:
    def __init__(self, theme='red_black'):
        """
        Initialize with theme selection
        theme: 'blue' or 'red_black' (default)
        """
        self.theme = theme
        
        # Company Information
        self.company_info = {
            "name": "PGT INTERNATIONAL (PRIVATE) LIMITED",
            "tagline": "Excellence in Transportation & Logistics",
            "address": "Office # 7, 1st Floor, Haji Yousuf Plaza, Near Memon Masjid, M.A Jinnah Road, Karachi",
            "phone": "+92-21-32412345",
            "mobile": "+92-300-1234567",
            "email": "info@pgtinternational.com",
            "website": "www.pgtinternational.com",
            "ntn": "NTN: 1234567-8",
            "bank_details": {
                "meezan": {
                    "bank_name": "Meezan Bank Limited",
                    "branch": "M.A. Jinnah Road Branch",
                    "account_title": "PGT International (Pvt) Ltd",
                    "account_number": "01234567890123",
                    "iban": "PK12 MEZN 0001 2345 6789 0123"
                },
                "faysal": {
                    "bank_name": "Faysal Bank Limited",
                    "branch": "Karachi Main Branch",
                    "account_title": "PGT International (Pvt) Ltd",
                    "account_number": "09876543210987",
                    "iban": "PK34 FAYS 0009 8765 4321 0987"
                }
            },
            "terms": [
                "Payment due within 7 days of invoice date",
                "Late payments subject to 2% monthly interest",
                "All disputes subject to Sahiwal Jurisdiction",
                "Goods remain property of PGT until full payment received"
            ]
        }
        
        # Theme Colors
        if theme == 'blue':
            self.colors = {
                'primary': colors.HexColor('#1e40af'),
                'secondary': colors.HexColor('#0ea5e9'),
                'accent': colors.HexColor('#1e293b'),
                'background': colors.HexColor('#f8fafc'),
                'text': colors.HexColor('#1f2937')
            }
        else:  # red_black
            self.colors = {
                'primary': colors.HexColor('#dc2626'),
                'secondary': colors.HexColor('#1f2937'),
                'accent': colors.HexColor('#ef4444'),
                'background': colors.HexColor('#ffffff'),
                'text': colors.HexColor('#1f2937')
            }
        
        # Logo path
        self.logo_path = Path("backend/static/logo.png")
        if not self.logo_path.exists():
            self.logo_path = None
    
    def create_logo_placeholder(self, width=1.2*inch, height=1.2*inch):
        """Create a simple logo placeholder if no logo file exists"""
        drawing = Drawing(width, height)
        
        # Background
        drawing.add(Rect(0, 0, width, height, 
                        fillColor=self.colors['primary'], 
                        strokeColor=None))
        
        # Text
        drawing.add(String(width/2, height/2, 'PGT',
                          fontSize=24,
                          fillColor=colors.white,
                          textAnchor='middle'))
        
        return drawing
    
    def generate_qr_code(self, invoice_number, amount):
        """Generate QR code for invoice verification"""
        qr_data = f"PGT-INV:{invoice_number}|AMT:{amount}|VERIFY:pgtinternational.com/verify"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Use string colors for QR code
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer
    
    def generate_commercial_invoice(
        self,
        invoice_data: Dict,
        client_data: Dict,
        trip_data: Dict,
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate modern commercial invoice PDF
        
        invoice_data: {
            'invoice_number': 'INV-2026-001',
            'invoice_date': '2026-02-27',
            'due_date': '2026-03-29',
            'payment_terms': 'Net 30 Days',
            'notes': 'Thank you for your business',
            'tax_amount': 0,
            'discount_amount': 0,
            'halting_charges': 500  # Optional
        }
        
        client_data: {
            'name': 'ABC Company Ltd',
            'contact_person': 'John Doe',
            'address': 'Client Address',
            'phone': '+92-XXX-XXXXXXX',
            'email': 'client@example.com'
        }
        
        trip_data: {
            'reference_no': 'TRP-2026-001',
            'bilty_no': 'BLT-2026-001',
            'container_no': 'CONT-2026-001',  # NEW: Container number
            'date': '2026-02-27',
            'vehicle_number': 'ABC-123',
            'driver_name': 'Muhammad Ali',
            'source_location': 'Karachi',
            'destination_location': 'Lahore',
            'category_product': 'General Goods',
            'total_tonnage': 25.5,
            'freight_mode': 'per_ton',
            'rate_per_ton': 2000,
            'client_freight': 51000
        }
        """
        buffer = BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(
            buffer if not output_path else output_path,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.4*inch,
            bottomMargin=0.4*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # ============================================
        # HEADER WITH LOGO AND COMPANY INFO
        # ============================================
        
        header_data = []
        
        if self.logo_path and self.logo_path.exists():
            logo = Image(str(self.logo_path), width=1*inch, height=1*inch)
        else:
            logo = self.create_logo_placeholder(1*inch, 1*inch)
        
        company_header = f"""
        <font size=18 color="{self.colors['primary'].hexval()}"><b>{self.company_info['name']}</b></font><br/>
        <font size=9 color="{self.colors['text'].hexval()}"><i>{self.company_info['tagline']}</i></font><br/>
        <font size=7 color="{self.colors['text'].hexval()}">
        {self.company_info['ntn']} | Phone: {self.company_info['phone']}<br/>
        Email: {self.company_info['email']} | Web: {self.company_info['website']}
        </font>
        """
        
        header_data = [[logo, Paragraph(company_header, styles['Normal'])]]
        header_table = Table(header_data, colWidths=[1.2*inch, 5.8*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        elements.append(header_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # Decorative line
        line_table = Table([['']], colWidths=[7*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 3, self.colors['primary']),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # INVOICE TITLE
        # ============================================
        
        invoice_title = f'<font size=20 color="{self.colors['primary'].hexval()}"><b>COMMERCIAL INVOICE</b></font>'
        elements.append(Paragraph(invoice_title, ParagraphStyle('InvoiceTitle', alignment=TA_CENTER)))
        elements.append(Spacer(1, 0.15*inch))
        
        # Invoice details header
        invoice_header_data = [[
            Paragraph(f'<font size=10><b>Invoice #:</b> {invoice_data["invoice_number"]}</font>', styles['Normal']),
            Paragraph(f'<font size=10><b>Date:</b> {invoice_data["invoice_date"]}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))
        ], [
            Paragraph(f'<font size=10><b>Due Date:</b> {invoice_data["due_date"]}</font>', styles['Normal']),
            Paragraph(f'<font size=10><b>Terms:</b> {invoice_data.get("payment_terms", "Net 30 Days")}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))
        ]]
        
        invoice_header_table = Table(invoice_header_data, colWidths=[3.5*inch, 3.5*inch])
        invoice_header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['background']),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('BOX', (0, 0), (-1, -1), 1, self.colors['text']),
        ]))
        elements.append(invoice_header_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # BILL TO & TRIP SUMMARY (SIDE BY SIDE)
        # ============================================
        
        bill_trip_data = [
            [
                Paragraph(f'<font size=10 color="{self.colors['primary'].hexval()}"><b>▓ BILL TO:</b></font>', styles['Normal']),
                Paragraph(f'<font size=10 color="{self.colors['primary'].hexval()}"><b>▓ TRIP SUMMARY:</b></font>', styles['Normal'])
            ],
            [
                Paragraph(f"""
                <font size=9>
                <b>{client_data['name']}</b><br/>
                Contact: {client_data.get('contact_person', 'N/A')}<br/>
                Phone: {client_data.get('phone', 'N/A')}<br/>
                Email: {client_data.get('email', 'N/A')}<br/>
                Address: {client_data.get('address', 'N/A')}
                </font>
                """, styles['Normal']),
                
                Paragraph(f"""
                <font size=9>
                <b>Vehicle #:</b> {trip_data.get('vehicle_number', 'N/A')}<br/>
                <b>Bilty #:</b> {trip_data.get('bilty_no', trip_data.get('reference_no', 'N/A'))}<br/>
                <b>Container #:</b> {trip_data.get('container_no', 'N/A')}<br/>
                <b>Route:</b> {trip_data.get('source_location', 'N/A')} → {trip_data.get('destination_location', 'N/A')}<br/>
                <b>Product:</b> {trip_data.get('category_product', 'N/A')}<br/>
                <b>Weight:</b> {trip_data.get('total_tonnage', 0):.2f} MT<br/>
                <b>Date:</b> {trip_data.get('date', 'N/A')}<br/>
                <b>Driver:</b> {trip_data.get('driver_name', 'N/A')}
                </font>
                """, styles['Normal'])
            ]
        ]
        
        bill_trip_table = Table(bill_trip_data, colWidths=[3.5*inch, 3.5*inch])
        bill_trip_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['background']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, self.colors['text']),
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.colors['text']),
        ]))
        elements.append(bill_trip_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # FINANCIAL BREAKDOWN
        # ============================================
        
        elements.append(Paragraph(f'<font size=11 color="{self.colors['primary'].hexval()}"><b>▓ FINANCIAL BREAKDOWN</b></font>', styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        charges_data = [
            [
                Paragraph('<font size=9 color="white"><b>Description</b></font>', styles['Normal']),
                Paragraph('<font size=9 color="white"><b>Rate</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph('<font size=9 color="white"><b>Weight/Qty</b></font>', ParagraphStyle('Center', alignment=TA_CENTER)),
                Paragraph('<font size=9 color="white"><b>Halting</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph('<font size=9 color="white"><b>Total</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ]
        ]
        
        # Main transportation charge
        service_desc = f"Transportation Service\nRoute: {trip_data.get('source_location', '')} → {trip_data.get('destination_location', '')}\nProduct: {trip_data.get('category_product', '')}"
        
        if trip_data.get('freight_mode') == 'per_ton':
            qty_text = f"{trip_data.get('tonnage', trip_data.get('total_tonnage', 0)):.2f} MT"
            rate_text = f"PKR {trip_data.get('rate_per_ton', 0):,.2f}/MT"
        else:
            qty_text = "1 Trip"
            rate_text = f"PKR {trip_data.get('client_freight', 0):,.2f}"
        
        amount = trip_data.get('client_freight', 0)
        halting_charges = invoice_data.get('halting_charges', 0)
        
        charges_data.append([
            Paragraph(f'<font size=8>{service_desc}</font>', styles['Normal']),
            Paragraph(f'<font size=8>{rate_text}</font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
            Paragraph(f'<font size=8>{qty_text}</font>', ParagraphStyle('Center', alignment=TA_CENTER)),
            Paragraph(f'<font size=8>{halting_charges:,.2f}</font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
            Paragraph(f'<font size=8><b>PKR {amount + halting_charges:,.2f}</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
        ])
        
        charges_table = Table(charges_data, colWidths=[2.5*inch, 1.2*inch, 1*inch, 0.8*inch, 1.5*inch])
        charges_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['text']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ]))
        elements.append(charges_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # TOTALS
        # ============================================
        
        subtotal = amount + halting_charges
        tax_amount = invoice_data.get('tax_amount', 0)
        discount_amount = invoice_data.get('discount_amount', 0)
        total_amount = subtotal + tax_amount - discount_amount
        
        totals_data = [
            ['', '', '', Paragraph('<font size=9><b>Subtotal:</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)), 
             Paragraph(f'<font size=9>PKR {subtotal:,.2f}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))],
        ]
        
        if tax_amount > 0:
            totals_data.append([
                '', '', '', Paragraph('<font size=9><b>GST (0%):</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph(f'<font size=9>PKR {tax_amount:,.2f}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ])
        
        if discount_amount > 0:
            totals_data.append([
                '', '', '', Paragraph('<font size=9><b>Discount:</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph(f'<font size=9>- PKR {discount_amount:,.2f}</font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ])
        
        totals_data.append([
            '', '', '', 
            Paragraph(f'<font size=12 color="{self.colors['primary'].hexval()}"><b>TOTAL DUE:</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
            Paragraph(f'<font size=12 color="{self.colors['primary'].hexval()}"><b>PKR {total_amount:,.2f}</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
        ])
        
        totals_table = Table(totals_data, colWidths=[2.5*inch, 1.2*inch, 1*inch, 0.8*inch, 1.5*inch])
        totals_table.setStyle(TableStyle([
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LINEABOVE', (2, -1), (-1, -1), 2, self.colors['primary']),
            ('BACKGROUND', (2, -1), (-1, -1), self.colors['background']),
        ]))
        elements.append(totals_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # PAYMENT INFORMATION WITH QR CODE
        # ============================================
        
        elements.append(Paragraph(f'<font size=11 color="{self.colors['primary'].hexval()}"><b>▓ PAYMENT INFORMATION</b></font>', styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Generate QR code
        qr_buffer = self.generate_qr_code(invoice_data['invoice_number'], total_amount)
        qr_image = Image(qr_buffer, width=1*inch, height=1*inch)
        
        payment_data = [[
            Paragraph(f"""
            <font size=8>
            <b>Bank Details (Meezan Bank):</b><br/>
            Bank: {self.company_info['bank_details']['meezan']['bank_name']}<br/>
            Branch: {self.company_info['bank_details']['meezan']['branch']}<br/>
            Account: {self.company_info['bank_details']['meezan']['account_title']}<br/>
            A/C #: {self.company_info['bank_details']['meezan']['account_number']}<br/>
            IBAN: {self.company_info['bank_details']['meezan']['iban']}<br/>
            <br/>
            <b>Bank Details (Faysal Bank):</b><br/>
            Bank: {self.company_info['bank_details']['faysal']['bank_name']}<br/>
            Branch: {self.company_info['bank_details']['faysal']['branch']}<br/>
            Account: {self.company_info['bank_details']['faysal']['account_title']}<br/>
            A/C #: {self.company_info['bank_details']['faysal']['account_number']}<br/>
            IBAN: {self.company_info['bank_details']['faysal']['iban']}<br/>
            <br/>
            <font color="{self.colors['accent'].hexval()}"><b>⚠️ IMPORTANT:</b> Quote Invoice # in payment reference</font>
            </font>
            """, styles['Normal']),
            qr_image
        ]]
        
        payment_table = Table(payment_data, colWidths=[5*inch, 2*inch])
        payment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['background']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 1, self.colors['text']),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ]))
        elements.append(payment_table)
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # TERMS & CONDITIONS
        # ============================================
        
        elements.append(Paragraph(f'<font size=10 color="{self.colors['primary'].hexval()}"><b>▓ TERMS & CONDITIONS</b></font>', styles['Normal']))
        elements.append(Spacer(1, 0.05*inch))
        
        terms_text = f"""
        <font size=7>
        • {self.company_info['terms'][0]}<br/>
        • {self.company_info['terms'][1]}<br/>
        • {self.company_info['terms'][2]}<br/>
        • {self.company_info['terms'][3]}
        </font>
        """
        elements.append(Paragraph(terms_text, styles['Normal']))
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # FOOTER
        # ============================================
        
        footer_line = Table([['']], colWidths=[7*inch])
        footer_line.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, self.colors['primary']),
        ]))
        elements.append(footer_line)
        elements.append(Spacer(1, 0.08*inch))
        
        footer_text = f"""
        <font size=8 color="{self.colors['text'].hexval()}">
        <b>Thank you for choosing PGT International!</b><br/>
        <br/>
        This is a digitally generated invoice. No signature required.<br/>
        For queries: {self.company_info['phone']} | {self.company_info['email']}<br/>
        <br/>
        Generated: {datetime.now().strftime('%d-%b-%Y %I:%M %p')} | Ref: {invoice_data['invoice_number']}<br/>
        <font color="{self.colors['accent'].hexval()}"><b>⚠️ NON-EDITABLE DOCUMENT</b> - Any alterations void this invoice</font>
        </font>
        """
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(elements)
        
        if not output_path:
            buffer.seek(0)
            return buffer
        return None
    
    def generate_invoice_from_trip_id(self, db, trip_id: int, theme: str = None) -> BytesIO:
        """
        Generate invoice directly from trip ID
        theme: 'blue' or 'red_black' (overrides instance theme)
        """
        if theme:
            self.theme = theme
            # Update colors based on theme
            if theme == 'blue':
                self.colors = {
                    'primary': colors.HexColor('#1e40af'),
                    'secondary': colors.HexColor('#0ea5e9'),
                    'accent': colors.HexColor('#1e293b'),
                    'background': colors.HexColor('#f8fafc'),
                    'text': colors.HexColor('#1f2937')
                }
            else:
                self.colors = {
                    'primary': colors.HexColor('#dc2626'),
                    'secondary': colors.HexColor('#1f2937'),
                    'accent': colors.HexColor('#ef4444'),
                    'background': colors.HexColor('#ffffff'),
                    'text': colors.HexColor('#1f2937')
                }
        
        import models
        
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
            'invoice_date': receivable.invoice_date.strftime('%d-%b-%Y'),
            'due_date': receivable.due_date.strftime('%d-%b-%Y'),
            'payment_terms': f'Net {receivable.payment_terms} Days',
            'notes': 'Thank you for your business!',
            'tax_amount': receivable.tax_amount or 0,
            'discount_amount': receivable.discount_amount or 0,
            'halting_charges': 0  # Can be added to trip model if needed
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
            'bilty_no': trip.reference_no,  # Can add separate bilty_no field if needed
            'container_no': f"CONT-{trip.reference_no.split('-')[-1]}" if trip.reference_no else 'N/A',
            'date': trip.date.strftime('%d-%b-%Y') if trip.date else 'N/A',
            'vehicle_number': trip.vehicle.vehicle_no if trip.vehicle else 'N/A',
            'driver_name': trip.driver_operator or 'N/A',
            'source_location': trip.source_location,
            'destination_location': trip.destination_location,
            'category_product': trip.category_product,
            'total_tonnage': float(trip.total_tonnage),
            'freight_mode': trip.freight_mode,
            'rate_per_ton': float(trip.rate_per_ton) if trip.rate_per_ton else 0,
            'tonnage': float(trip.tonnage) if trip.tonnage else float(trip.total_tonnage),
            'client_freight': float(trip.client_freight)
        }
        
        # Generate PDF
        return self.generate_commercial_invoice(
            invoice_data=invoice_data,
            client_data=client_data,
            trip_data=trip_data
        )


# Create singleton instances for both themes
modern_invoice_generator_blue = ModernInvoiceGenerator(theme='blue')
modern_invoice_generator_red = ModernInvoiceGenerator(theme='red_black')

# Default to red/black theme
modern_invoice_generator = modern_invoice_generator_red

"""
Staff Advance Ledger Generator - Bank Statement Style
Professional ledger with running balance for Muhammad Hussain and other staff
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
from pathlib import Path

class StaffLedgerGenerator:
    def __init__(self):
        self.company_info = {
            "name": "PGT INTERNATIONAL (PRIVATE) LIMITED",
            "tagline": "Staff Advance Recovery Statement",
            "address": "Office # 7, 1st Floor, Haji Yousuf Plaza, M.A Jinnah Road, Karachi",
            "phone": "+92-21-32412345",
            "email": "info@pgtinternational.com"
        }
        
        # Red/Black theme
        self.colors = {
            'primary': colors.HexColor('#dc2626'),
            'secondary': colors.HexColor('#1f2937'),
            'accent': colors.HexColor('#ef4444'),
            'background': colors.HexColor('#f8fafc'),
            'text': colors.HexColor('#1f2937'),
            'positive': colors.HexColor('#059669'),
            'negative': colors.HexColor('#dc2626')
        }
        
        # Logo path
        self.logo_path = Path("backend/static/logo.png")
        if not self.logo_path.exists():
            self.logo_path = None
    
    def generate_staff_recovery_statement(
        self,
        staff_data: Dict,
        transactions: List[Dict],
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate bank statement style staff advance recovery statement
        
        staff_data: {
            'name': 'Muhammad Hussain',
            'employee_id': 'EMP-001',
            'position': 'Driver',
            'opening_balance': 140000,
            'current_balance': 120000,
            'monthly_deduction': 5000
        }
        
        transactions: [
            {
                'date': '2026-01-15',
                'description': 'Advance Given',
                'debit': 50000,
                'credit': 0,
                'balance': 50000
            },
            {
                'date': '2026-01-31',
                'description': 'Salary Deduction - January',
                'debit': 0,
                'credit': 5000,
                'balance': 45000
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
            topMargin=0.4*inch,
            bottomMargin=0.4*inch
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # ============================================
        # HEADER
        # ============================================
        
        if self.logo_path and self.logo_path.exists():
            logo = Image(str(self.logo_path), width=0.8*inch, height=0.8*inch)
        else:
            # Simple placeholder
            from reportlab.graphics.shapes import Drawing, Rect, String
            drawing = Drawing(0.8*inch, 0.8*inch)
            drawing.add(Rect(0, 0, 0.8*inch, 0.8*inch, 
                            fillColor=self.colors['primary'], 
                            strokeColor=None))
            drawing.add(String(0.4*inch, 0.4*inch, 'PGT',
                              fontSize=18,
                              fillColor=colors.white,
                              textAnchor='middle'))
            logo = drawing
        
        company_header = f"""
        <font size=16 color="{self.colors['primary'].hexval()}"><b>{self.company_info['name']}</b></font><br/>
        <font size=10 color="{self.colors['text'].hexval()}"><b>{self.company_info['tagline']}</b></font><br/>
        <font size=7 color="{self.colors['text'].hexval()}">
        {self.company_info['address']}<br/>
        Phone: {self.company_info['phone']} | Email: {self.company_info['email']}
        </font>
        """
        
        header_data = [[logo, Paragraph(company_header, styles['Normal'])]]
        header_table = Table(header_data, colWidths=[1*inch, 6*inch])
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
        elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # STATEMENT TITLE
        # ============================================
        
        title = f'<font size=18 color="{self.colors['primary'].hexval()}"><b>STAFF ADVANCE RECOVERY STATEMENT</b></font>'
        elements.append(Paragraph(title, ParagraphStyle('Title', alignment=TA_CENTER)))
        elements.append(Spacer(1, 0.15*inch))
        
        # ============================================
        # STAFF INFORMATION BOX
        # ============================================
        
        staff_info_data = [
            [
                Paragraph(f'<font size=10 color="{self.colors['primary'].hexval()}"><b>STAFF DETAILS</b></font>', styles['Normal']),
                Paragraph(f'<font size=10 color="{self.colors['primary'].hexval()}"><b>ACCOUNT SUMMARY</b></font>', styles['Normal'])
            ],
            [
                Paragraph(f"""
                <font size=9>
                <b>Name:</b> {staff_data['name']}<br/>
                <b>Employee ID:</b> {staff_data['employee_id']}<br/>
                <b>Position:</b> {staff_data['position']}<br/>
                <b>Monthly Deduction:</b> PKR {staff_data.get('monthly_deduction', 0):,.2f}
                </font>
                """, styles['Normal']),
                
                Paragraph(f"""
                <font size=9>
                <b>Opening Balance:</b> PKR {staff_data.get('opening_balance', 0):,.2f}<br/>
                <b>Total Advances:</b> PKR {sum(t.get('debit', 0) for t in transactions):,.2f}<br/>
                <b>Total Recovered:</b> PKR {sum(t.get('credit', 0) for t in transactions):,.2f}<br/>
                <b>Current Balance:</b> <font color="{self.colors['negative'].hexval()}"><b>PKR {staff_data.get('current_balance', 0):,.2f}</b></font>
                </font>
                """, styles['Normal'])
            ]
        ]
        
        staff_info_table = Table(staff_info_data, colWidths=[3.5*inch, 3.5*inch])
        staff_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['background']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, self.colors['text']),
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.colors['text']),
        ]))
        elements.append(staff_info_table)
        elements.append(Spacer(1, 0.25*inch))
        
        # ============================================
        # TRANSACTION HISTORY (BANK STATEMENT STYLE)
        # ============================================
        
        elements.append(Paragraph(f'<font size=11 color="{self.colors['primary'].hexval()}"><b>▓ TRANSACTION HISTORY</b></font>', styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Table header
        trans_data = [
            [
                Paragraph('<font size=9 color="white"><b>Date</b></font>', styles['Normal']),
                Paragraph('<font size=9 color="white"><b>Description</b></font>', styles['Normal']),
                Paragraph('<font size=9 color="white"><b>Advance Given</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph('<font size=9 color="white"><b>Recovery</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph('<font size=9 color="white"><b>Running Balance</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ]
        ]
        
        # Add transactions
        for trans in transactions:
            date_str = trans.get('date', '')
            if isinstance(date_str, datetime):
                date_str = date_str.strftime('%d-%b-%Y')
            
            debit = trans.get('debit', 0)
            credit = trans.get('credit', 0)
            balance = trans.get('balance', 0)
            
            # Color code the balance (red if outstanding)
            balance_color = self.colors['negative'].hexval() if balance > 0 else self.colors['positive'].hexval()
            
            debit_str = f"{debit:,.2f}" if debit > 0 else "-"
            credit_str = f"{credit:,.2f}" if credit > 0 else "-"
            
            trans_data.append([
                Paragraph(f'<font size=8>{date_str}</font>', styles['Normal']),
                Paragraph(f'<font size=8>{trans.get("description", "")}</font>', styles['Normal']),
                Paragraph(f'<font size=8>{debit_str}</font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph(f'<font size=8>{credit_str}</font>', ParagraphStyle('Right', alignment=TA_RIGHT)),
                Paragraph(f'<font size=8 color="{balance_color}"><b>{balance:,.2f}</b></font>', ParagraphStyle('Right', alignment=TA_RIGHT))
            ])
        
        trans_table = Table(trans_data, colWidths=[1*inch, 2.5*inch, 1.2*inch, 1.2*inch, 1.1*inch])
        trans_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colors['text']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colors['background']]),
        ]))
        elements.append(trans_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # RECOVERY SCHEDULE
        # ============================================
        
        if staff_data.get('monthly_deduction', 0) > 0 and staff_data.get('current_balance', 0) > 0:
            elements.append(Paragraph(f'<font size=11 color="{self.colors['primary'].hexval()}"><b>▓ RECOVERY SCHEDULE</b></font>', styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
            
            months_remaining = int(staff_data['current_balance'] / staff_data['monthly_deduction'])
            final_payment = staff_data['current_balance'] % staff_data['monthly_deduction']
            
            schedule_text = f"""
            <font size=9>
            <b>Monthly Deduction:</b> PKR {staff_data['monthly_deduction']:,.2f}<br/>
            <b>Months Remaining:</b> {months_remaining} months<br/>
            <b>Final Payment:</b> PKR {final_payment:,.2f}<br/>
            <b>Expected Completion:</b> {months_remaining + (1 if final_payment > 0 else 0)} months from now
            </font>
            """
            
            schedule_box = Paragraph(schedule_text, styles['Normal'])
            schedule_table = Table([[schedule_box]], colWidths=[7*inch])
            schedule_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), self.colors['background']),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('BOX', (0, 0), (-1, -1), 1, self.colors['text']),
            ]))
            elements.append(schedule_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # ============================================
        # IMPORTANT NOTES
        # ============================================
        
        elements.append(Paragraph(f'<font size=10 color="{self.colors['primary'].hexval()}"><b>▓ IMPORTANT NOTES</b></font>', styles['Normal']))
        elements.append(Spacer(1, 0.05*inch))
        
        notes_text = """
        <font size=7>
        • This statement is system-generated and requires no signature<br/>
        • All advances are deducted from monthly salary as per company policy<br/>
        • Running balance shows outstanding amount after each transaction<br/>
        • For any discrepancies, contact HR within 7 days of statement date<br/>
        • This document is for record purposes only and cannot be altered
        </font>
        """
        elements.append(Paragraph(notes_text, styles['Normal']))
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
        <b>PGT International (Private) Limited</b><br/>
        This is a digitally generated statement. No signature required.<br/>
        For queries: {self.company_info['phone']} | {self.company_info['email']}<br/>
        <br/>
        Generated: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}<br/>
        <font color="{self.colors['accent'].hexval()}"><b>⚠️ NON-EDITABLE DOCUMENT</b> - Any alterations void this statement</font>
        </font>
        """
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(elements)
        
        if not output_path:
            buffer.seek(0)
            return buffer
        return None
    
    def generate_from_staff_id(self, db, staff_id: int) -> BytesIO:
        """Generate statement from staff ID"""
        import models
        
        # Get staff
        staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
        if not staff:
            raise ValueError(f"Staff {staff_id} not found")
        
        # Get transactions
        ledger_entries = db.query(models.StaffAdvanceLedger).filter(
            models.StaffAdvanceLedger.staff_id == staff_id
        ).order_by(models.StaffAdvanceLedger.transaction_date).all()
        
        # Prepare staff data
        staff_data = {
            'name': staff.name,
            'employee_id': staff.employee_id,
            'position': staff.position,
            'opening_balance': 0,  # Calculate from first transaction
            'current_balance': staff.advance_balance,
            'monthly_deduction': staff.monthly_deduction
        }
        
        # Prepare transactions
        transactions = []
        for entry in ledger_entries:
            transactions.append({
                'date': entry.transaction_date,
                'description': entry.description or entry.transaction_type.replace('_', ' ').title(),
                'debit': entry.amount if entry.amount > 0 else 0,
                'credit': abs(entry.amount) if entry.amount < 0 else 0,
                'balance': entry.balance_after
            })
        
        if transactions:
            staff_data['opening_balance'] = transactions[0]['balance'] - transactions[0]['debit'] + transactions[0]['credit']
        
        # Generate PDF
        return self.generate_staff_recovery_statement(
            staff_data=staff_data,
            transactions=transactions
        )


# Create singleton instance
staff_ledger_generator = StaffLedgerGenerator()

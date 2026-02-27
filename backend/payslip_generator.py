"""
Payslip Generator Service
Professional payslip generation for staff
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from datetime import datetime
from io import BytesIO
from typing import Optional, Dict
import calendar

class PayslipGenerator:
    def __init__(self):
        self.company_info = {
            "name": "PGT International (Private) Limited",
            "address": "Main Office Address, City, Country",
            "phone": "+92-XXX-XXXXXXX",
            "email": "hr@pgtinternational.com"
        }
    
    def generate_payslip_pdf(
        self,
        staff_data: Dict,
        payroll_data: Dict,
        output_path: Optional[str] = None
    ) -> BytesIO:
        """
        Generate professional payslip PDF
        
        staff_data: {
            'employee_id': 'EMP001',
            'name': 'John Doe',
            'position': 'Driver',
            'bank_account': '1234567890'
        }
        
        payroll_data: {
            'month': 2,
            'year': 2026,
            'gross_salary': 50000,
            'arrears': 5000,
            'advance_deduction': 10000,
            'other_deductions': 2000,
            'net_payable': 43000,
            'payment_date': '2026-02-28'
        }
        """
        buffer = BytesIO()
        
        # Create PDF
        doc = SimpleDocTemplate(
            buffer if not output_path else output_path,
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=20,
            textColor=colors.HexColor('#dc2626'),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#6b7280'),
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        # Company Header
        elements.append(Paragraph(self.company_info['name'], title_style))
        elements.append(Paragraph(self.company_info['address'], subtitle_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Payslip Title
        month_name = calendar.month_name[payroll_data['month']]
        payslip_title = f'<font size=16 color="#374151"><b>PAYSLIP - {month_name} {payroll_data["year"]}</b></font>'
        elements.append(Paragraph(payslip_title, ParagraphStyle('PayslipTitle', alignment=TA_CENTER)))
        elements.append(Spacer(1, 0.3*inch))
        
        # Employee Details
        emp_details_data = [
            ['Employee Details', ''],
            ['Employee ID:', staff_data['employee_id']],
            ['Name:', staff_data['name']],
            ['Position:', staff_data['position']],
            ['Bank Account:', staff_data.get('bank_account', 'N/A')],
            ['Payment Date:', payroll_data.get('payment_date', 'N/A')]
        ]
        
        emp_table = Table(emp_details_data, colWidths=[2.5*inch, 4*inch])
        emp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f9fafb')),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#374151')),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 1), (0, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb'))
        ]))
        elements.append(emp_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Earnings and Deductions
        earnings_deductions_data = [
            ['Earnings', 'Amount (PKR)', 'Deductions', 'Amount (PKR)'],
            [
                'Basic Salary',
                f"{payroll_data['gross_salary']:,.2f}",
                'Advance Deduction',
                f"{payroll_data['advance_deduction']:,.2f}"
            ],
            [
                'Arrears',
                f"{payroll_data['arrears']:,.2f}",
                'Other Deductions',
                f"{payroll_data['other_deductions']:,.2f}"
            ],
            [
                '',
                '',
                '',
                ''
            ],
            [
                'Total Earnings',
                f"{payroll_data['gross_salary'] + payroll_data['arrears']:,.2f}",
                'Total Deductions',
                f"{payroll_data['advance_deduction'] + payroll_data['other_deductions']:,.2f}"
            ]
        ]
        
        earnings_table = Table(earnings_deductions_data, colWidths=[2*inch, 1.25*inch, 2*inch, 1.25*inch])
        earnings_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#374151')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -2), colors.HexColor('#374151')),
            ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -2), 10),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#f3f4f6')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -1), (-1, -1), 11),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
            ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#374151'))
        ]))
        elements.append(earnings_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Net Payable
        net_payable_data = [
            ['NET PAYABLE', f"PKR {payroll_data['net_payable']:,.2f}"]
        ]
        
        net_table = Table(net_payable_data, colWidths=[4.25*inch, 2.25*inch])
        net_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.whitesmoke),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12)
        ]))
        elements.append(net_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Footer
        footer_text = """
        <font size=8 color="#6b7280">
        <b>Note:</b> This is a computer-generated payslip and does not require a signature.<br/>
        For any queries, please contact the HR department.<br/><br/>
        <b>Confidential:</b> This payslip is confidential and intended solely for the named employee.
        </font>
        """
        elements.append(Paragraph(footer_text, ParagraphStyle('Footer', alignment=TA_CENTER)))
        
        # Build PDF
        doc.build(elements)
        
        if not output_path:
            buffer.seek(0)
            return buffer
        
        return None
    
    def generate_bulk_payslips(self, payroll_entries: list, output_dir: str = "payslips"):
        """Generate payslips for multiple employees"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        results = []
        for entry in payroll_entries:
            try:
                filename = f"{output_dir}/payslip_{entry['staff_data']['employee_id']}_{entry['payroll_data']['year']}_{entry['payroll_data']['month']:02d}.pdf"
                self.generate_payslip_pdf(
                    staff_data=entry['staff_data'],
                    payroll_data=entry['payroll_data'],
                    output_path=filename
                )
                results.append({
                    'success': True,
                    'employee_id': entry['staff_data']['employee_id'],
                    'filename': filename
                })
            except Exception as e:
                results.append({
                    'success': False,
                    'employee_id': entry['staff_data']['employee_id'],
                    'error': str(e)
                })
        
        return results

# Singleton instance
payslip_generator = PayslipGenerator()

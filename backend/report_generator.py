#!/usr/bin/env python3
"""
Report Generator - PDF and Excel export functionality for PGT TMS
Generates professional reports with print-ready layouts and company branding
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import pandas as pd
from io import BytesIO
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import os
from company_config import get_company_info, get_company_header

class ReportGenerator:
    """
    Professional report generator for PGT TMS
    Supports PDF and Excel export with company branding
    """
    
    def __init__(self):
        self.company_info = get_company_info()
        self.company_header = get_company_header()
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for reports"""
        # Company header style
        self.styles.add(ParagraphStyle(
            name='CompanyHeader',
            parent=self.styles['Heading1'],
            fontSize=18,
            spaceAfter=4,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#dc2626'),
            fontName='Helvetica-Bold'
        ))
        
        # Company tagline style
        self.styles.add(ParagraphStyle(
            name='CompanyTagline',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=2,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#6b7280'),
            fontName='Helvetica-Oblique'
        ))
        
        # Company address style
        self.styles.add(ParagraphStyle(
            name='CompanyAddress',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=2,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#374151')
        ))
        
        # Report title style
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#374151'),
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=6,
            textColor=colors.HexColor('#1f2937'),
            fontName='Helvetica-Bold'
        ))
        
        # Summary style
        self.styles.add(ParagraphStyle(
            name='Summary',
            parent=self.styles['Normal'],
            fontSize=9,
            spaceAfter=6,
            textColor=colors.HexColor('#6b7280')
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#9ca3af')
        ))
    
    def create_header(self, doc_title: str, date_range: str = None) -> List:
        """Create standard report header with company branding"""
        elements = []
        
        # Add logo if exists
        logo_path = self.company_info.get('logo_path')
        if logo_path and os.path.exists(logo_path):
            try:
                logo = Image(logo_path, width=1.5*inch, height=0.75*inch)
                elements.append(logo)
                elements.append(Spacer(1, 6))
            except:
                pass  # Skip logo if file not found
        
        # Company name
        elements.append(Paragraph(self.company_info['name'], self.styles['CompanyHeader']))
        
        # Company tagline
        if 'tagline' in self.company_info:
            elements.append(Paragraph(self.company_info['tagline'], self.styles['CompanyTagline']))
        
        # Company address
        elements.append(Paragraph(self.company_info['address'], self.styles['CompanyAddress']))
        
        # Contact information
        contact_info = f"Phone: {self.company_info['phone']} | Email: {self.company_info['email']} | Web: {self.company_info['website']}"
        elements.append(Paragraph(contact_info, self.styles['CompanyAddress']))
        
        # Separator line
        elements.append(Spacer(1, 12))
        line_table = Table([['']], colWidths=[7*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#dc2626')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 12))
        
        # Report title
        elements.append(Paragraph(doc_title, self.styles['ReportTitle']))
        
        # Date range if provided
        if date_range:
            elements.append(Paragraph(f"<b>Period:</b> {date_range}", self.styles['Summary']))
        
        # Generation date
        elements.append(Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", 
            self.styles['Summary']
        ))
        elements.append(Spacer(1, 20))
        
        return elements
    
    def create_footer(self) -> Paragraph:
        """Create standard report footer"""
        footer_text = f"{self.company_info['name']} | {self.company_info['website']} | Page <pageNumber/>"
        return Paragraph(footer_text, self.styles['Footer'])
    
    def format_currency(self, amount: float) -> str:
        """Format currency in PKR"""
        return f"PKR {amount:,.2f}"
    
    def add_excel_header(self, worksheet, workbook, title: str, date_range: str = None):
        """Add professional header to Excel worksheet"""
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': '#dc2626',
            'align': 'center',
            'valign': 'vcenter'
        })
        
        tagline_format = workbook.add_format({
            'font_size': 9,
            'italic': True,
            'font_color': '#6b7280',
            'align': 'center'
        })
        
        address_format = workbook.add_format({
            'font_size': 9,
            'font_color': '#374151',
            'align': 'center'
        })
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'font_color': '#374151',
            'align': 'center',
            'valign': 'vcenter',
            'top': 2,
            'bottom': 2
        })
        
        info_format = workbook.add_format({
            'font_size': 9,
            'font_color': '#6b7280',
            'align': 'center'
        })
        
        # Set row heights
        worksheet.set_row(0, 24)
        worksheet.set_row(1, 15)
        worksheet.set_row(2, 15)
        worksheet.set_row(3, 15)
        worksheet.set_row(4, 3)
        worksheet.set_row(5, 20)
        worksheet.set_row(6, 15)
        worksheet.set_row(7, 15)
        worksheet.set_row(8, 3)
        
        # Company name
        worksheet.merge_range('A1:K1', self.company_info['name'], header_format)
        
        # Tagline
        if 'tagline' in self.company_info:
            worksheet.merge_range('A2:K2', self.company_info['tagline'], tagline_format)
        
        # Address
        worksheet.merge_range('A3:K3', self.company_info['address'], address_format)
        
        # Contact
        contact_info = f"Phone: {self.company_info['phone']} | Email: {self.company_info['email']} | Web: {self.company_info['website']}"
        worksheet.merge_range('A4:K4', contact_info, address_format)
        
        # Empty row
        worksheet.merge_range('A5:K5', '', address_format)
        
        # Report title
        worksheet.merge_range('A6:K6', title, title_format)
        
        # Date range
        if date_range:
            worksheet.merge_range('A7:K7', f"Period: {date_range}", info_format)
        
        # Generation date
        gen_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        worksheet.merge_range('A8:K8', f"Generated: {gen_date}", info_format)
        
        # Empty row before data
        worksheet.merge_range('A9:K9', '', info_format)
        
        return 9  # Return the row number where data should start
    
    def generate_vendor_ledger_pdf(self, vendor_data: Dict, ledger_entries: List[Dict]) -> BytesIO:
            """
            Generate enhanced vendor ledger PDF report with international standards
            - Quick Info Box (top right)
            - Monthly transaction grouping
            - Color-coded payment status
            - Running balance always visible
            """
            from collections import defaultdict
            from calendar import month_name

            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

            elements = []

            # Header
            elements.extend(self.create_header(
                f"Vendor Ledger Statement - {vendor_data['name']}", 
                f"As of {datetime.now().strftime('%B %d, %Y')}"
            ))

            # ENHANCEMENT 1: Quick Info Box (Top Right)
            outstanding = vendor_data.get('current_balance', 0)
            last_payment = vendor_data.get('last_payment_date', 'No payments')
            if isinstance(last_payment, (date, datetime)):
                last_payment = last_payment.strftime('%d-%b-%Y')

            # Determine status
            if outstanding > 0:
                status = 'OVERDUE'
                status_color = colors.HexColor('#dc2626')  # Red
            elif outstanding < 0:
                status = 'CREDIT BALANCE'
                status_color = colors.HexColor('#16a34a')  # Green
            else:
                status = 'SETTLED'
                status_color = colors.HexColor('#16a34a')  # Green

            quick_info_data = [
                ['ACCOUNT SUMMARY'],
                ['Total Outstanding:', self.format_currency(outstanding)],
                ['Last Payment:', str(last_payment)],
                ['Status:', status]
            ]

            quick_info_table = Table(quick_info_data, colWidths=[1.5*inch, 1.5*inch])
            quick_info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('SPAN', (0, 0), (-1, 0)),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BACKGROUND', (0, 1), (0, -1), colors.HexColor('#f3f4f6')),
                ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#dc2626') if outstanding > 0 else colors.black),
                ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
                ('TEXTCOLOR', (1, 3), (1, 3), status_color),
                ('FONTNAME', (1, 3), (1, 3), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))

            elements.append(quick_info_table)
            elements.append(Spacer(1, 20))

            # Vendor contact information
            vendor_info = [
                ['Vendor Code:', vendor_data.get('vendor_code', 'N/A')],
                ['Contact Person:', vendor_data.get('contact_person', 'N/A')],
                ['Phone:', vendor_data.get('phone', 'N/A')],
                ['Email:', vendor_data.get('email', 'N/A')]
            ]

            vendor_table = Table(vendor_info, colWidths=[2*inch, 3*inch])
            vendor_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))

            elements.append(vendor_table)
            elements.append(Spacer(1, 20))

            # ENHANCEMENT 2 & 3: Monthly Grouping + Color-Coded Status
            elements.append(Paragraph("Transaction History", self.styles['SectionHeader']))

            if ledger_entries:
                # Group entries by month
                monthly_groups = defaultdict(list)
                for entry in ledger_entries:
                    entry_date = entry.get('date')
                    if isinstance(entry_date, str):
                        try:
                            entry_date = datetime.strptime(entry_date, '%Y-%m-%d')
                        except:
                            entry_date = datetime.now()
                    elif not isinstance(entry_date, (date, datetime)):
                        entry_date = datetime.now()

                    month_key = (entry_date.year, entry_date.month)
                    monthly_groups[month_key].append(entry)

                # Sort months chronologically
                sorted_months = sorted(monthly_groups.keys())

                for year, month in sorted_months:
                    # Month header
                    month_header = f"{month_name[month].upper()} {year}"
                    elements.append(Spacer(1, 10))
                    elements.append(Paragraph(month_header, self.styles['SectionHeader']))

                    # Table headers
                    ledger_data = [['Date', 'Description', 'Reference', 'Debit', 'Credit', 'Balance', 'Status']]

                    month_debit = 0
                    month_credit = 0

                    # Add entries for this month
                    for entry in monthly_groups[(year, month)]:
                        entry_date = entry.get('date')
                        if isinstance(entry_date, (date, datetime)):
                            date_str = entry_date.strftime('%d-%b')
                        else:
                            date_str = str(entry_date)

                        debit = entry.get('debit_amount', 0)
                        credit = entry.get('credit_amount', 0)
                        balance = entry.get('running_balance', 0)

                        month_debit += debit
                        month_credit += credit

                        # Determine payment status
                        if credit > 0:
                            status = 'Paid'
                        elif debit > 0:
                            status = 'Pending'
                        else:
                            status = '-'

                        ledger_data.append([
                            date_str,
                            entry.get('description', ''),
                            entry.get('reference_no', ''),
                            self.format_currency(debit) if debit > 0 else '',
                            self.format_currency(credit) if credit > 0 else '',
                            self.format_currency(balance),
                            status
                        ])

                    # Month subtotal row
                    ledger_data.append([
                        '',
                        f'{month_name[month].upper()} TOTAL:',
                        '',
                        self.format_currency(month_debit) if month_debit > 0 else '',
                        self.format_currency(month_credit) if month_credit > 0 else '',
                        '',
                        ''
                    ])

                    ledger_table = Table(ledger_data, colWidths=[0.7*inch, 2*inch, 0.8*inch, 0.9*inch, 0.9*inch, 0.9*inch, 0.7*inch])
                    ledger_table.setStyle(TableStyle([
                        # Header row
                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('ALIGN', (1, 1), (1, -2), 'LEFT'),  # Description left-aligned
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                        ('FONTSIZE', (0, 0), (-1, -1), 8),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f9fafb')]),
                        # Subtotal row
                        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e5e7eb')),
                        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                        ('SPAN', (0, -1), (1, -1)),
                        ('ALIGN', (0, -1), (1, -1), 'RIGHT'),
                    ]))

                    # Color-code status column
                    for i in range(1, len(ledger_data) - 1):  # Skip header and subtotal
                        status = ledger_data[i][6]
                        if status == 'Paid':
                            ledger_table.setStyle(TableStyle([
                                ('BACKGROUND', (6, i), (6, i), colors.HexColor('#d1fae5')),
                                ('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#065f46')),
                            ]))
                        elif status == 'Pending':
                            ledger_table.setStyle(TableStyle([
                                ('BACKGROUND', (6, i), (6, i), colors.HexColor('#fee2e2')),
                                ('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#991b1b')),
                            ]))

                    elements.append(ledger_table)
            else:
                elements.append(Paragraph("No transactions found for this vendor.", self.styles['Summary']))

            # Summary
            elements.append(Spacer(1, 20))
            summary_data = [
                ['Total Transactions:', str(len(ledger_entries))],
                ['Current Balance:', self.format_currency(vendor_data.get('current_balance', 0))],
                ['Status:', 'Active' if vendor_data.get('is_active', True) else 'Inactive']
            ]

            summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(summary_table)

            doc.build(elements)
            buffer.seek(0)
            return buffer

    
    def generate_staff_payroll_pdf(self, staff_data: List[Dict], payroll_entries: List[Dict], period: str) -> BytesIO:
        """Generate staff payroll PDF report"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        elements = []
        
        # Header
        elements.extend(self.create_header(f"Staff Payroll Report", period))
        
        # Summary
        total_gross = sum(entry.get('gross_salary', 0) for entry in payroll_entries)
        total_deductions = sum(entry.get('advance_deduction', 0) + entry.get('other_deductions', 0) for entry in payroll_entries)
        total_net = sum(entry.get('net_payable', 0) for entry in payroll_entries)
        
        summary_data = [
            ['Total Staff:', str(len(staff_data))],
            ['Total Gross Salary:', self.format_currency(total_gross)],
            ['Total Deductions:', self.format_currency(total_deductions)],
            ['Total Net Payable:', self.format_currency(total_net)]
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Payroll details
        elements.append(Paragraph("Payroll Details", self.styles['SectionHeader']))
        
        if payroll_entries:
            payroll_data = [['Staff Name', 'Employee ID', 'Gross Salary', 'Advance Deduction', 'Other Deductions', 'Net Payable']]
            
            for entry in payroll_entries:
                # Find staff info
                staff_info = next((s for s in staff_data if s.get('id') == entry.get('staff_id')), {})
                payroll_data.append([
                    staff_info.get('name', 'Unknown'),
                    staff_info.get('employee_id', 'N/A'),
                    self.format_currency(entry.get('gross_salary', 0)),
                    self.format_currency(entry.get('advance_deduction', 0)),
                    self.format_currency(entry.get('other_deductions', 0)),
                    self.format_currency(entry.get('net_payable', 0))
                ])
            
            payroll_table = Table(payroll_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            payroll_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),  # Staff name left-aligned
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')])
            ]))
            
            elements.append(payroll_table)
        else:
            elements.append(Paragraph("No payroll entries found for this period.", self.styles['Summary']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_financial_summary_pdf(self, financial_data: Dict) -> BytesIO:
        """Generate financial summary PDF report"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        elements = []
        
        # Header
        elements.extend(self.create_header("Financial Summary Report", f"As of {datetime.now().strftime('%B %d, %Y')}"))
        
        # Key metrics
        elements.append(Paragraph("Key Financial Metrics", self.styles['SectionHeader']))
        
        metrics_data = [
            ['Net Profit:', self.format_currency(financial_data.get('net_profit', 0))],
            ['Total Income:', self.format_currency(financial_data.get('total_income', 0))],
            ['Total Expenses:', self.format_currency(financial_data.get('total_expenses', 0))],
            ['Profit Margin:', f"{financial_data.get('profit_margin', 0):.1f}%"],
            ['Total Receivables:', self.format_currency(financial_data.get('total_receivables', 0))],
            ['Total Payables:', self.format_currency(financial_data.get('total_payables', 0))],
            ['Cash/Bank Balance:', self.format_currency(financial_data.get('cash_bank_balance', 0))]
        ]
        
        metrics_table = Table(metrics_data, colWidths=[2.5*inch, 2.5*inch])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 20))
        
        # Daily cash flow
        elements.append(Paragraph("Today's Cash Flow", self.styles['SectionHeader']))
        
        cash_flow_data = [
            ['Daily Income:', self.format_currency(financial_data.get('daily_income', 0))],
            ['Daily Outgoing:', self.format_currency(financial_data.get('daily_outgoing', 0))],
            ['Daily Net:', self.format_currency(financial_data.get('daily_net', 0))]
        ]
        
        cash_flow_table = Table(cash_flow_data, colWidths=[2.5*inch, 2.5*inch])
        cash_flow_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(cash_flow_table)
        elements.append(Spacer(1, 20))
        
        # Fleet metrics
        elements.append(Paragraph("Fleet Operations", self.styles['SectionHeader']))
        
        fleet_data = [
            ['Active Vehicles:', str(financial_data.get('active_vehicles', 0))],
            ['Total Trips:', str(financial_data.get('total_trips', 0))],
            ['Monthly Trips:', str(financial_data.get('monthly_trips', 0))]
        ]
        
        fleet_table = Table(fleet_data, colWidths=[2.5*inch, 2.5*inch])
        fleet_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        elements.append(fleet_table)
        
        # Alerts if any
        if financial_data.get('alerts'):
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("Financial Alerts", self.styles['SectionHeader']))
            
            for alert in financial_data['alerts']:
                elements.append(Paragraph(f"• {alert.get('title', '')}: {alert.get('message', '')}", self.styles['Summary']))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_excel_export(self, data: List[Dict], filename: str, sheet_name: str = "Data") -> BytesIO:
        """Generate Excel export from data"""
        buffer = BytesIO()
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        
        # Create Excel writer
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        buffer.seek(0)
        return buffer
    def generate_payables_report_pdf(self, payables_data):
        """Generate comprehensive payables report PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Header
        elements.extend(self.create_header("PAYABLES REPORT", f"As of {datetime.now().strftime('%B %d, %Y')}"))
        
        # Summary section
        total_payables = sum(float(p.get('outstanding_amount', 0)) for p in payables_data)
        overdue_payables = sum(float(p.get('outstanding_amount', 0)) for p in payables_data if p.get('is_overdue', False))
        
        summary_data = [
            ['Total Outstanding Payables:', self.format_currency(total_payables)],
            ['Overdue Payables:', self.format_currency(overdue_payables)],
            ['Total Vendors:', str(len(payables_data))],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Detailed payables table
        if payables_data:
            # Table headers
            headers = ['Vendor', 'Contact', 'Outstanding Amount', 'Last Payment', 'Status']
            
            # Table data
            table_data = [headers]
            for payable in payables_data:
                row = [
                    payable.get('vendor_name', 'N/A'),
                    payable.get('vendor_phone', 'N/A'),
                    self.format_currency(float(payable.get('outstanding_amount', 0))),
                    payable.get('last_payment_date', 'Never'),
                    'Overdue' if payable.get('is_overdue', False) else 'Current'
                ]
                table_data.append(row)
            
            # Create table
            table = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1.3*inch, 1.2*inch, 1*inch])
            table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No payables data available.", self.styles['Summary']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_receivables_report_pdf(self, receivables_data):
        """Generate comprehensive receivables report PDF"""
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch)
        
        # Container for the 'Flowable' objects
        elements = []
        
        # Header
        elements.extend(self.create_header("RECEIVABLES REPORT", f"As of {datetime.now().strftime('%B %d, %Y')}"))
        
        # Summary section
        total_receivables = sum(float(r.get('outstanding_amount', 0)) for r in receivables_data)
        overdue_receivables = sum(float(r.get('outstanding_amount', 0)) for r in receivables_data if r.get('is_overdue', False))
        
        summary_data = [
            ['Total Outstanding Receivables:', self.format_currency(total_receivables)],
            ['Overdue Receivables:', self.format_currency(overdue_receivables)],
            ['Total Clients:', str(len(receivables_data))],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Detailed receivables table
        if receivables_data:
            # Table headers
            headers = ['Client', 'Contact', 'Outstanding Amount', 'Last Payment', 'Status']
            
            # Table data
            table_data = [headers]
            for receivable in receivables_data:
                row = [
                    receivable.get('client_name', 'N/A'),
                    receivable.get('client_phone', 'N/A'),
                    self.format_currency(float(receivable.get('outstanding_amount', 0))),
                    receivable.get('last_payment_date', 'Never'),
                    'Overdue' if receivable.get('is_overdue', False) else 'Current'
                ]
                table_data.append(row)
            
            # Create table
            table = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1.3*inch, 1.2*inch, 1*inch])
            table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16a34a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # Alternating row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph("No receivables data available.", self.styles['Summary']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer

    def generate_payables_excel(self, payables_data):
        """Generate payables Excel report"""
        try:
            import xlsxwriter
        except ImportError:
            # Fallback to pandas if xlsxwriter not available
            return self.generate_excel_export(payables_data, "payables_report", "Payables")
        
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Create worksheet
        worksheet = workbook.add_worksheet('Payables Report')
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#dc2626',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        currency_format = workbook.add_format({
            'num_format': 'PKR #,##0.00',
            'align': 'right',
            'border': 1
        })
        
        text_format = workbook.add_format({
            'align': 'left',
            'border': 1
        })
        
        # Write title
        worksheet.merge_range('A1:F1', 'PAYABLES REPORT', header_format)
        worksheet.write('A2', f'Generated on: {datetime.now().strftime("%B %d, %Y")}', text_format)
        
        # Write headers
        headers = ['Vendor Name', 'Vendor Code', 'Contact Person', 'Phone', 'Outstanding Amount', 'Status']
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, header_format)
        
        # Write data
        row = 4
        total_outstanding = 0
        for payable in payables_data:
            worksheet.write(row, 0, payable.get('vendor_name', ''), text_format)
            worksheet.write(row, 1, payable.get('vendor_code', ''), text_format)
            worksheet.write(row, 2, payable.get('vendor_contact', ''), text_format)
            worksheet.write(row, 3, payable.get('vendor_phone', ''), text_format)
            
            outstanding = float(payable.get('outstanding_amount', 0))
            worksheet.write(row, 4, outstanding, currency_format)
            total_outstanding += outstanding
            
            status = 'Overdue' if payable.get('is_overdue', False) else 'Current'
            worksheet.write(row, 5, status, text_format)
            row += 1
        
        # Write total
        worksheet.write(row + 1, 3, 'TOTAL:', header_format)
        worksheet.write(row + 1, 4, total_outstanding, currency_format)
        
        # Adjust column widths
        worksheet.set_column('A:A', 20)  # Vendor Name
        worksheet.set_column('B:B', 15)  # Vendor Code
        worksheet.set_column('C:C', 18)  # Contact Person
        worksheet.set_column('D:D', 15)  # Phone
        worksheet.set_column('E:E', 18)  # Outstanding Amount
        worksheet.set_column('F:F', 12)  # Status
        
        workbook.close()
        output.seek(0)
        return output

    def generate_receivables_excel(self, receivables_data):
        """Generate receivables Excel report"""
        try:
            import xlsxwriter
        except ImportError:
            # Fallback to pandas if xlsxwriter not available
            return self.generate_excel_export(receivables_data, "receivables_report", "Receivables")
        
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Create worksheet
        worksheet = workbook.add_worksheet('Receivables Report')
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'bg_color': '#16a34a',
            'font_color': 'white',
            'align': 'center',
            'valign': 'vcenter',
            'border': 1
        })
        
        currency_format = workbook.add_format({
            'num_format': 'PKR #,##0.00',
            'align': 'right',
            'border': 1
        })
        
        text_format = workbook.add_format({
            'align': 'left',
            'border': 1
        })
        
        # Write title
        worksheet.merge_range('A1:F1', 'RECEIVABLES REPORT', header_format)
        worksheet.write('A2', f'Generated on: {datetime.now().strftime("%B %d, %Y")}', text_format)
        
        # Write headers
        headers = ['Client Name', 'Client Code', 'Contact Person', 'Phone', 'Outstanding Amount', 'Status']
        for col, header in enumerate(headers):
            worksheet.write(3, col, header, header_format)
        
        # Write data
        row = 4
        total_outstanding = 0
        for receivable in receivables_data:
            worksheet.write(row, 0, receivable.get('client_name', ''), text_format)
            worksheet.write(row, 1, receivable.get('client_code', ''), text_format)
            worksheet.write(row, 2, receivable.get('client_contact', ''), text_format)
            worksheet.write(row, 3, receivable.get('client_phone', ''), text_format)
            
            outstanding = float(receivable.get('outstanding_amount', 0))
            worksheet.write(row, 4, outstanding, currency_format)
            total_outstanding += outstanding
            
            status = 'Overdue' if receivable.get('is_overdue', False) else 'Current'
            worksheet.write(row, 5, status, text_format)
            row += 1
        
        # Write total
        worksheet.write(row + 1, 3, 'TOTAL:', header_format)
        worksheet.write(row + 1, 4, total_outstanding, currency_format)
        
        # Adjust column widths
        worksheet.set_column('A:A', 20)  # Client Name
        worksheet.set_column('B:B', 15)  # Client Code
        worksheet.set_column('C:C', 18)  # Contact Person
        worksheet.set_column('D:D', 15)  # Phone
        worksheet.set_column('E:E', 18)  # Outstanding Amount
        worksheet.set_column('F:F', 12)  # Status
        
        workbook.close()
        output.seek(0)
        return output
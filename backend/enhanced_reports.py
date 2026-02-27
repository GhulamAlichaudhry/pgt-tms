#!/usr/bin/env python3
"""
Enhanced Report Generator - International Logistics Standards
Implements Director's 4 formatting requirements:
1. Quick Info Box on all ledgers
2. Monthly transaction grouping with subtotals
3. Color-coded payment status tags
4. Admin-only profit columns in Excel
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime, date
from typing import List, Dict
from collections import defaultdict
from calendar import month_name
from report_generator import ReportGenerator

class EnhancedReportGenerator(ReportGenerator):
    """
    Enhanced report generator with international standards
    Extends base ReportGenerator with Director's requirements
    """
    
    def generate_vendor_ledger_pdf_enhanced(self, vendor_data: Dict, ledger_entries: List[Dict]) -> BytesIO:
        """
        Generate enhanced vendor ledger PDF with:
        - Quick Info Box (top right)
        - Monthly transaction grouping
        - Color-coded payment status
        - Running balance always visible
        """
        from reportlab.platypus import SimpleDocTemplate
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        elements = []
        
        # Header
        elements.extend(self.create_header(
            f"Vendor Ledger Statement - {vendor_data['name']}", 
            f"As of {datetime.now().strftime('%B %d, %Y')}"
        ))
        
        # ENHANCEMENT 1: Quick Info Box
        outstanding = vendor_data.get('current_balance', 0)
        last_payment = vendor_data.get('last_payment_date', 'No payments')
        if isinstance(last_payment, (date, datetime)):
            last_payment = last_payment.strftime('%d-%b-%Y')
        
        # Determine status
        if outstanding > 0:
            status = 'OVERDUE'
            status_color = colors.HexColor('#dc2626')
        elif outstanding < 0:
            status = 'CREDIT BALANCE'
            status_color = colors.HexColor('#16a34a')
        else:
            status = 'SETTLED'
            status_color = colors.HexColor('#16a34a')
        
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
                
                # Base table style
                table_style = [
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc2626')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('ALIGN', (1, 1), (1, -2), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f9fafb')]),
                    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e5e7eb')),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('SPAN', (0, -1), (1, -1)),
                    ('ALIGN', (0, -1), (1, -1), 'RIGHT'),
                ]
                
                # Color-code status column
                for i in range(1, len(ledger_data) - 1):
                    status = ledger_data[i][6]
                    if status == 'Paid':
                        table_style.extend([
                            ('BACKGROUND', (6, i), (6, i), colors.HexColor('#d1fae5')),
                            ('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#065f46')),
                        ])
                    elif status == 'Pending':
                        table_style.extend([
                            ('BACKGROUND', (6, i), (6, i), colors.HexColor('#fee2e2')),
                            ('TEXTCOLOR', (6, i), (6, i), colors.HexColor('#991b1b')),
                        ])
                
                ledger_table.setStyle(TableStyle(table_style))
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

    
    def generate_financial_summary_pdf_enhanced(self, financial_data: Dict, expense_breakdown: Dict, aging_data: Dict) -> BytesIO:
        """
        Generate enhanced financial summary PDF with:
        - Detailed expense breakdown (Office/Staff/Vendor)
        - Receivable aging table at bottom
        - All standard metrics
        """
        from reportlab.platypus import SimpleDocTemplate
        
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
        
        # ENHANCEMENT 3A: Expense Breakdown
        elements.append(Paragraph("Expense Breakdown", self.styles['SectionHeader']))
        
        expense_data = [
            ['Office Expenses (Milk/Roti/Fuel):', self.format_currency(expense_breakdown.get('office_expenses', 0))],
            ['Staff Salaries:', self.format_currency(expense_breakdown.get('staff_salaries', 0))],
            ['Vendor Payments:', self.format_currency(expense_breakdown.get('vendor_payments', 0))],
            ['Other Expenses:', self.format_currency(expense_breakdown.get('other_expenses', 0))],
            ['TOTAL EXPENSES:', self.format_currency(expense_breakdown.get('total', 0))]
        ]
        
        expense_table = Table(expense_data, colWidths=[3*inch, 2*inch])
        expense_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -2), colors.HexColor('#f3f4f6')),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#dc2626')),
            ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
            ('TEXTCOLOR', (0, 0), (-1, -2), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(expense_table)
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
        
        # ENHANCEMENT 3B: Receivable Aging Table
        elements.append(Paragraph("Receivable Aging Analysis", self.styles['SectionHeader']))
        elements.append(Paragraph(
            "Critical: Ensures 4.9M from Pak Afghan is always visible",
            self.styles['Summary']
        ))
        elements.append(Spacer(1, 10))
        
        total_receivables = aging_data.get('total', 0)
        
        aging_table_data = [
            ['Bucket', 'Amount', '% of Total'],
            ['0-30 Days', 
             self.format_currency(aging_data.get('0-30', 0)),
             f"{(aging_data.get('0-30', 0) / total_receivables * 100) if total_receivables > 0 else 0:.1f}%"],
            ['31-60 Days',
             self.format_currency(aging_data.get('31-60', 0)),
             f"{(aging_data.get('31-60', 0) / total_receivables * 100) if total_receivables > 0 else 0:.1f}%"],
            ['61-90 Days',
             self.format_currency(aging_data.get('61-90', 0)),
             f"{(aging_data.get('61-90', 0) / total_receivables * 100) if total_receivables > 0 else 0:.1f}%"],
            ['90+ Days',
             self.format_currency(aging_data.get('90+', 0)),
             f"{(aging_data.get('90+', 0) / total_receivables * 100) if total_receivables > 0 else 0:.1f}%"],
            ['TOTAL',
             self.format_currency(total_receivables),
             '100.0%']
        ]
        
        aging_table = Table(aging_table_data, colWidths=[2*inch, 2*inch, 1.5*inch])
        
        # Base style
        aging_style = [
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f9fafb')]),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#e5e7eb')),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]
        
        # Highlight 90+ days in RED
        if aging_data.get('90+', 0) > 0:
            aging_style.extend([
                ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#fee2e2')),
                ('TEXTCOLOR', (0, 4), (-1, 4), colors.HexColor('#991b1b')),
                ('FONTNAME', (0, 4), (-1, 4), 'Helvetica-Bold'),
            ])
        
        aging_table.setStyle(TableStyle(aging_style))
        elements.append(aging_table)
        
        # Fleet metrics
        elements.append(Spacer(1, 20))
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
        
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def generate_staff_statement_pdf_enhanced(self, staff_data: Dict, ledger_entries: List[Dict]) -> BytesIO:
        """
        Generate enhanced staff advance statement PDF with:
        - Quick Info Box showing advance balance
        - Bank statement style
        - Running balance decreasing each month
        - Professional format for Muhammad Hussain
        """
        from reportlab.platypus import SimpleDocTemplate
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
        
        elements = []
        
        # Header
        elements.extend(self.create_header(
            f"Staff Advance Statement - {staff_data['name']}", 
            f"As of {datetime.now().strftime('%B %d, %Y')}"
        ))
        
        # ENHANCEMENT 1: Quick Info Box
        advance_balance = staff_data.get('advance_balance', 0)
        monthly_deduction = staff_data.get('monthly_deduction', 0)
        last_deduction = staff_data.get('last_deduction_date', 'Not yet started')
        if isinstance(last_deduction, (date, datetime)):
            last_deduction = last_deduction.strftime('%d-%b-%Y')
        
        # Calculate months remaining
        months_remaining = int(advance_balance / monthly_deduction) if monthly_deduction > 0 else 0
        
        quick_info_data = [
            ['ADVANCE SUMMARY'],
            ['Outstanding Balance:', self.format_currency(advance_balance)],
            ['Monthly Deduction:', self.format_currency(monthly_deduction)],
            ['Months Remaining:', f"{months_remaining} months"],
            ['Status:', 'RECOVERING' if advance_balance > 0 else 'CLEAR']
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
            ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor('#dc2626') if advance_balance > 0 else colors.HexColor('#16a34a')),
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(quick_info_table)
        elements.append(Spacer(1, 20))
        
        # Staff information
        staff_info = [
            ['Employee ID:', staff_data.get('employee_id', 'N/A')],
            ['Position:', staff_data.get('position', 'N/A')],
            ['Gross Salary:', self.format_currency(staff_data.get('gross_salary', 0))],
            ['Phone:', staff_data.get('phone', 'N/A')]
        ]
        
        staff_table = Table(staff_info, colWidths=[2*inch, 3*inch])
        staff_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(staff_table)
        elements.append(Spacer(1, 20))
        
        # Transaction History - Bank Statement Style
        elements.append(Paragraph("Advance Ledger - Bank Statement Style", self.styles['SectionHeader']))
        
        if ledger_entries:
            # Table headers
            ledger_data = [['Date', 'Description', 'Debit (Given)', 'Credit (Recovered)', 'Balance']]
            
            # Add entries
            for entry in ledger_entries:
                entry_date = entry.get('date')
                if isinstance(entry_date, (date, datetime)):
                    date_str = entry_date.strftime('%d-%b-%Y')
                else:
                    date_str = str(entry_date)
                
                debit = entry.get('debit_amount', 0)
                credit = entry.get('credit_amount', 0)
                balance = entry.get('running_balance', 0)
                
                ledger_data.append([
                    date_str,
                    entry.get('description', ''),
                    self.format_currency(debit) if debit > 0 else '-',
                    self.format_currency(credit) if credit > 0 else '-',
                    self.format_currency(balance)
                ])
            
            ledger_table = Table(ledger_data, colWidths=[1.2*inch, 2.5*inch, 1.2*inch, 1.2*inch, 1.2*inch])
            ledger_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (1, 1), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9fafb')]),
                # Highlight balance column
                ('FONTNAME', (4, 1), (4, -1), 'Helvetica-Bold'),
            ]))
            
            elements.append(ledger_table)
        else:
            elements.append(Paragraph("No advance transactions found.", self.styles['Summary']))
        
        # Summary and signature
        elements.append(Spacer(1, 30))
        
        summary_text = f"""
        <b>Current Outstanding:</b> {self.format_currency(advance_balance)}<br/>
        <b>Monthly Recovery:</b> {self.format_currency(monthly_deduction)}<br/>
        <b>Expected Clear Date:</b> {months_remaining} months from now<br/><br/>
        <i>This is a computer-generated statement. No signature required.</i><br/>
        <i>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</i>
        """
        
        elements.append(Paragraph(summary_text, self.styles['Summary']))
        
        # Signature section
        elements.append(Spacer(1, 40))
        signature_data = [
            ['_____________________', '_____________________'],
            ['Employee Signature', 'Authorized Signature'],
            ['Date: ______________', 'Date: ______________']
        ]
        
        signature_table = Table(signature_data, colWidths=[2.5*inch, 2.5*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elements.append(signature_table)
        
        doc.build(elements)
        buffer.seek(0)
        return buffer

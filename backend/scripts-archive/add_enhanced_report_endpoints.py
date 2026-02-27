#!/usr/bin/env python3
"""
Script to add enhanced report endpoints to main.py
Run this to integrate Director's international standards
"""

enhanced_endpoints = '''

# ============================================
# ENHANCED REPORT ENDPOINTS - INTERNATIONAL STANDARDS
# ============================================

@app.get("/reports/vendor-ledger-pdf-enhanced/{vendor_id}")
def generate_vendor_ledger_pdf_enhanced(
    vendor_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Generate ENHANCED vendor ledger PDF with:
    - Quick Info Box (top right)
    - Monthly transaction grouping
    - Color-coded payment status
    - Running balance always visible
    """
    from fastapi.responses import StreamingResponse
    from enhanced_reports import EnhancedReportGenerator
    from datetime import datetime
    
    # Get vendor data
    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    
    # Get last payment date
    last_payment = db.query(models.Payable).filter(
        models.Payable.vendor_id == vendor_id,
        models.Payable.outstanding_amount < models.Payable.amount
    ).order_by(models.Payable.date.desc()).first()
    
    last_payment_date = last_payment.date if last_payment else None
    
    # Get ledger entries
    ledger_entries = []
    try:
        # Get payables for this vendor
        payables = db.query(models.Payable).filter(
            models.Payable.vendor_id == vendor_id
        ).order_by(models.Payable.date).all()
        
        running_balance = 0
        for payable in payables:
            # Debit entry (new payable)
            running_balance += float(payable.amount)
            ledger_entries.append({
                "date": payable.date,
                "description": f"Invoice {payable.invoice_number}",
                "reference_no": payable.invoice_number,
                "debit_amount": float(payable.amount),
                "credit_amount": 0,
                "running_balance": running_balance
            })
            
            # Credit entry (payment made)
            if payable.amount > payable.outstanding_amount:
                paid_amount = float(payable.amount - payable.outstanding_amount)
                running_balance -= paid_amount
                ledger_entries.append({
                    "date": payable.date,
                    "description": f"Payment for {payable.invoice_number}",
                    "reference_no": f"PAY-{payable.invoice_number}",
                    "debit_amount": 0,
                    "credit_amount": paid_amount,
                    "running_balance": running_balance
                })
    except Exception as e:
        print(f"Warning: Could not fetch ledger entries: {e}")
    
    # Convert to dict format
    vendor_data = {
        "name": vendor.name,
        "vendor_code": f"VEN-{vendor.id:04d}",
        "contact_person": vendor.contact_person,
        "phone": vendor.phone,
        "email": getattr(vendor, 'email', ''),
        "current_balance": float(vendor.current_balance),
        "last_payment_date": last_payment_date,
        "is_active": vendor.is_active
    }
    
    # Generate enhanced PDF
    generator = EnhancedReportGenerator()
    pdf_buffer = generator.generate_vendor_ledger_pdf_enhanced(vendor_data, ledger_entries)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Ledger_{datetime.now().strftime('%Y-%m-%d')}_{vendor.name.replace(' ', '_')}.pdf"}
    )

@app.get("/reports/financial-summary-pdf-enhanced")
def generate_financial_summary_pdf_enhanced(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.require_role([models.UserRole.ADMIN]))
):
    """
    Generate ENHANCED financial summary PDF with:
    - Detailed expense breakdown (Office/Staff/Vendor)
    - Receivable aging table at bottom
    - All standard metrics
    """
    from fastapi.responses import StreamingResponse
    from enhanced_reports import EnhancedReportGenerator
    from financial_calculator import FinancialCalculator
    from datetime import datetime, date, timedelta
    
    calculator = FinancialCalculator(db)
    
    try:
        # Get financial summary
        financial_data = calculator.get_master_financial_summary()
        
        # ENHANCEMENT: Get expense breakdown
        # Office expenses
        office_expenses = db.query(func.sum(models.OfficeExpense.amount)).filter(
            models.OfficeExpense.date >= date.today().replace(day=1)
        ).scalar() or 0
        
        # Staff salaries (current month)
        staff_salaries = db.query(func.sum(models.Staff.gross_salary)).scalar() or 0
        
        # Vendor payments (current month)
        vendor_payments = db.query(
            func.sum(models.Payable.amount - models.Payable.outstanding_amount)
        ).filter(
            models.Payable.date >= date.today().replace(day=1)
        ).scalar() or 0
        
        expense_breakdown = {
            "office_expenses": float(office_expenses),
            "staff_salaries": float(staff_salaries),
            "vendor_payments": float(vendor_payments),
            "other_expenses": 0,
            "total": float(office_expenses + staff_salaries + vendor_payments)
        }
        
        # ENHANCEMENT: Get receivable aging
        receivables = db.query(models.Receivable).filter(
            models.Receivable.remaining_amount > 0
        ).all()
        
        aging_buckets = {
            "0-30": 0,
            "31-60": 0,
            "61-90": 0,
            "90+": 0,
            "total": 0
        }
        
        for receivable in receivables:
            days_old = (date.today() - receivable.invoice_date).days
            amount = float(receivable.remaining_amount)
            aging_buckets["total"] += amount
            
            if days_old <= 30:
                aging_buckets["0-30"] += amount
            elif days_old <= 60:
                aging_buckets["31-60"] += amount
            elif days_old <= 90:
                aging_buckets["61-90"] += amount
            else:
                aging_buckets["90+"] += amount
        
        # Generate enhanced PDF
        generator = EnhancedReportGenerator()
        pdf_buffer = generator.generate_financial_summary_pdf_enhanced(
            financial_data,
            expense_breakdown,
            aging_buckets
        )
        
        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Financial_Summary_{datetime.now().strftime('%Y-%m-%d')}.pdf"}
        )
    finally:
        calculator.close()

@app.get("/reports/staff-statement-pdf-enhanced/{staff_id}")
def generate_staff_statement_pdf_enhanced(
    staff_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Generate ENHANCED staff advance statement PDF with:
    - Quick Info Box showing advance balance
    - Bank statement style
    - Running balance decreasing each month
    - Professional format
    """
    from fastapi.responses import StreamingResponse
    from enhanced_reports import EnhancedReportGenerator
    from datetime import datetime
    
    # Get staff data
    staff = db.query(models.Staff).filter(models.Staff.id == staff_id).first()
    if not staff:
        raise HTTPException(status_code=404, detail="Staff member not found")
    
    # Get advance ledger entries
    ledger_entries = db.query(models.StaffAdvanceLedger).filter(
        models.StaffAdvanceLedger.staff_id == staff_id
    ).order_by(models.StaffAdvanceLedger.transaction_date).all()
    
    # Get last deduction date
    last_deduction = db.query(models.StaffAdvanceLedger).filter(
        models.StaffAdvanceLedger.staff_id == staff_id,
        models.StaffAdvanceLedger.transaction_type == 'recovery'
    ).order_by(models.StaffAdvanceLedger.transaction_date.desc()).first()
    
    # Convert to dict format
    staff_data = {
        "name": staff.name,
        "employee_id": staff.employee_id,
        "position": staff.position,
        "gross_salary": float(staff.gross_salary),
        "advance_balance": float(staff.advance_balance),
        "monthly_deduction": float(staff.monthly_deduction),
        "phone": getattr(staff, 'phone', 'N/A'),
        "last_deduction_date": last_deduction.transaction_date if last_deduction else None
    }
    
    ledger_data = []
    for entry in ledger_entries:
        ledger_data.append({
            "date": entry.transaction_date,
            "description": entry.description,
            "debit_amount": float(entry.debit_amount),
            "credit_amount": float(entry.credit_amount),
            "running_balance": float(entry.balance_after)
        })
    
    # Generate enhanced PDF
    generator = EnhancedReportGenerator()
    pdf_buffer = generator.generate_staff_statement_pdf_enhanced(staff_data, ledger_data)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=Staff_Statement_{datetime.now().strftime('%Y-%m-%d')}_{staff.name.replace(' ', '_')}.pdf"}
    )
'''

print("Enhanced report endpoints code generated.")
print("\nTo integrate:")
print("1. Copy the code above")
print("2. Add to backend/main.py after existing report endpoints")
print("3. Restart backend server")
print("\nNew endpoints:")
print("- GET /reports/vendor-ledger-pdf-enhanced/{vendor_id}")
print("- GET /reports/financial-summary-pdf-enhanced")
print("- GET /reports/staff-statement-pdf-enhanced/{staff_id}")

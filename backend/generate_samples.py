"""
Generate Sample Documents for Director's Review
Run this to create sample Trip Invoice and Hussain Recovery Statement
"""
from modern_invoice_generator import modern_invoice_generator
from staff_ledger_generator import staff_ledger_generator
from database import SessionLocal
from datetime import datetime, timedelta

def generate_sample_invoice():
    """Generate sample trip invoice"""
    print("📄 Generating Sample Trip Invoice...")
    
    # Sample data
    invoice_data = {
        'invoice_number': 'INV-2026-001',
        'invoice_date': datetime.now().strftime('%d-%b-%Y'),
        'due_date': (datetime.now() + timedelta(days=7)).strftime('%d-%b-%Y'),
        'payment_terms': 'Net 7 Days',
        'notes': 'Thank you for your business!',
        'tax_amount': 0,
        'discount_amount': 0,
        'halting_charges': 500
    }
    
    client_data = {
        'name': 'Fauji Foods Limited',
        'contact_person': 'Mr. Ahmed Khan',
        'address': 'Plot # 123, Industrial Area, Karachi',
        'phone': '+92-21-34567890',
        'email': 'ahmed.khan@faujifoods.com'
    }
    
    trip_data = {
        'reference_no': 'TRP-2026-001',
        'bilty_no': 'BLT-2026-001',
        'container_no': 'CONT-2026-001',
        'date': datetime.now().strftime('%d-%b-%Y'),
        'vehicle_number': 'KHI-1234',
        'driver_name': 'Muhammad Ali',
        'source_location': 'Karachi',
        'destination_location': 'Lahore',
        'category_product': 'Food Products',
        'total_tonnage': 25.5,
        'freight_mode': 'per_ton',
        'rate_per_ton': 16156.86,  # 412,000 / 25.5
        'tonnage': 25.5,
        'client_freight': 412000
    }
    
    # Generate PDF
    pdf_buffer = modern_invoice_generator.generate_commercial_invoice(
        invoice_data=invoice_data,
        client_data=client_data,
        trip_data=trip_data
    )
    
    # Save to file
    with open('SAMPLE_TRIP_INVOICE.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    print("✅ Sample Trip Invoice generated: SAMPLE_TRIP_INVOICE.pdf")
    print(f"   - Invoice #: {invoice_data['invoice_number']}")
    print(f"   - Client: {client_data['name']}")
    print(f"   - Amount: PKR {trip_data['client_freight']:,.2f}")
    print(f"   - Halting: PKR {invoice_data['halting_charges']:,.2f}")
    print(f"   - Total: PKR {trip_data['client_freight'] + invoice_data['halting_charges']:,.2f}")
    print()

def generate_sample_hussain_statement():
    """Generate sample Muhammad Hussain recovery statement"""
    print("📊 Generating Sample Hussain Recovery Statement...")
    
    # Sample staff data
    staff_data = {
        'name': 'Muhammad Hussain',
        'employee_id': 'EMP-001',
        'position': 'Senior Driver',
        'opening_balance': 0,
        'current_balance': 140000,
        'monthly_deduction': 5000
    }
    
    # Sample transactions
    transactions = [
        {
            'date': '15-Jan-2026',
            'description': 'Advance Given - Emergency',
            'debit': 50000,
            'credit': 0,
            'balance': 50000
        },
        {
            'date': '31-Jan-2026',
            'description': 'Salary Deduction - January 2026',
            'debit': 0,
            'credit': 5000,
            'balance': 45000
        },
        {
            'date': '28-Feb-2026',
            'description': 'Salary Deduction - February 2026',
            'debit': 0,
            'credit': 5000,
            'balance': 40000
        },
        {
            'date': '15-Mar-2026',
            'description': 'Advance Given - Family Emergency',
            'debit': 100000,
            'credit': 0,
            'balance': 140000
        }
    ]
    
    # Generate PDF
    pdf_buffer = staff_ledger_generator.generate_staff_recovery_statement(
        staff_data=staff_data,
        transactions=transactions
    )
    
    # Save to file
    with open('SAMPLE_HUSSAIN_STATEMENT.pdf', 'wb') as f:
        f.write(pdf_buffer.getvalue())
    
    print("✅ Sample Hussain Statement generated: SAMPLE_HUSSAIN_STATEMENT.pdf")
    print(f"   - Employee: {staff_data['name']} ({staff_data['employee_id']})")
    print(f"   - Position: {staff_data['position']}")
    print(f"   - Current Balance: PKR {staff_data['current_balance']:,.2f}")
    print(f"   - Monthly Deduction: PKR {staff_data['monthly_deduction']:,.2f}")
    print(f"   - Months Remaining: {int(staff_data['current_balance'] / staff_data['monthly_deduction'])}")
    print()

def main():
    """Generate all sample documents"""
    print("=" * 60)
    print("PGT INTERNATIONAL - SAMPLE DOCUMENT GENERATOR")
    print("=" * 60)
    print()
    
    try:
        # Generate invoice
        generate_sample_invoice()
        
        # Generate Hussain statement
        generate_sample_hussain_statement()
        
        print("=" * 60)
        print("✅ ALL SAMPLE DOCUMENTS GENERATED SUCCESSFULLY!")
        print("=" * 60)
        print()
        print("📁 Files created:")
        print("   1. SAMPLE_TRIP_INVOICE.pdf")
        print("   2. SAMPLE_HUSSAIN_STATEMENT.pdf")
        print()
        print("📋 Next Steps:")
        print("   1. Open the PDF files to review")
        print("   2. Verify against log book records")
        print("   3. Check all calculations")
        print("   4. Review with Director for final sign-off")
        print()
        print("🎨 Theme: PGT Red/Black Applied")
        print("🔒 Security: Non-Editable PDFs")
        print("📱 QR Codes: Included for verification")
        print()
        
    except Exception as e:
        print(f"❌ Error generating samples: {str(e)}")
        print()
        print("Troubleshooting:")
        print("1. Make sure qrcode library is installed: pip install qrcode[pil]")
        print("2. Check that backend/static/ folder exists")
        print("3. Verify database connection")
        print()

if __name__ == "__main__":
    main()

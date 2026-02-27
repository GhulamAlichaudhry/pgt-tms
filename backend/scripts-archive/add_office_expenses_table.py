"""
Add office_expenses table to database
Run this script to create the office expenses tracking table
"""

from database import engine, SessionLocal
from models import Base, OfficeExpense
from sqlalchemy import inspect

def add_office_expenses_table():
    """Create office_expenses table if it doesn't exist"""
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if 'office_expenses' in existing_tables:
        print("✓ office_expenses table already exists")
        return
    
    print("Creating office_expenses table...")
    
    # Create only the OfficeExpense table
    OfficeExpense.__table__.create(engine, checkfirst=True)
    
    print("✓ office_expenses table created successfully!")
    print("\nTable structure:")
    print("- id: Primary key")
    print("- date: Date of entry")
    print("- entry_type: 'expense' or 'cash_received'")
    print("- account_title: Category or 'Cash Received'")
    print("- particulars: Description")
    print("- amount_received: Amount received (default 0)")
    print("- amount_paid: Amount paid (default 0)")
    print("- created_at: Timestamp")
    print("- created_by: User ID")

if __name__ == "__main__":
    print("=" * 60)
    print("Office Expenses Table Migration")
    print("=" * 60)
    print()
    
    add_office_expenses_table()
    
    print()
    print("=" * 60)
    print("Migration Complete!")
    print("=" * 60)

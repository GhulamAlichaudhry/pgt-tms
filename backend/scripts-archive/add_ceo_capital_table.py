"""
Add CEO Capital table to database
Run this script to create the CEO Capital tracking system
"""

from database import engine, SessionLocal
from models import Base, CEOCapital
from sqlalchemy import inspect
from datetime import date

def add_ceo_capital_table():
    """Create ceo_capital table if it doesn't exist"""
    
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    if 'ceo_capital' in existing_tables:
        print("✓ ceo_capital table already exists")
        return True
    
    print("Creating ceo_capital table...")
    
    # Create only the CEOCapital table
    CEOCapital.__table__.create(engine, checkfirst=True)
    
    print("✓ ceo_capital table created successfully!")
    print("\nTable structure:")
    print("- id: Primary key")
    print("- date: Transaction date")
    print("- transaction_type: Type of transaction")
    print("- description: Transaction description")
    print("- amount_in: Money coming in")
    print("- amount_out: Money going out")
    print("- balance: Running balance")
    print("- reference_id: Link to source record")
    print("- reference_type: Type of source")
    print("- created_at: Timestamp")
    print("- created_by: User ID")
    print("- notes: Additional notes")
    
    return True

def set_opening_balance(amount: float, opening_date: str = None):
    """
    Set opening balance for CEO Capital
    
    Args:
        amount: Opening balance amount
        opening_date: Date for opening balance (format: YYYY-MM-DD)
    """
    db = SessionLocal()
    
    try:
        # Use provided date or first day of current month
        if opening_date:
            balance_date = date.fromisoformat(opening_date)
        else:
            today = date.today()
            balance_date = date(today.year, today.month, 1)
        
        # Check if opening balance already exists
        existing = db.query(CEOCapital).filter(
            CEOCapital.transaction_type == "opening_balance"
        ).first()
        
        if existing:
            print(f"\n✗ Opening balance already exists")
            print(f"  Date: {existing.date}")
            print(f"  Amount: PKR {existing.balance:,.2f}")
            
            update = input("\nDo you want to update it? (yes/no): ").lower()
            if update == 'yes':
                existing.date = balance_date
                existing.amount_in = amount
                existing.balance = amount
                existing.description = f"Opening Balance - Updated"
                db.commit()
                print(f"✓ Opening balance updated to PKR {amount:,.2f}")
            else:
                print("✗ No changes made")
            return
        
        # Create opening balance entry
        opening_balance = CEOCapital(
            date=balance_date,
            transaction_type='opening_balance',
            description='CEO Capital - Opening Balance',
            amount_in=amount,
            amount_out=0.0,
            balance=amount,
            reference_id=None,
            reference_type=None,
            created_by=1,  # Admin user
            notes='Initial CEO Capital balance'
        )
        
        db.add(opening_balance)
        db.commit()
        
        print(f"\n✓ CEO Capital opening balance set successfully!")
        print(f"  Date: {balance_date}")
        print(f"  Amount: PKR {amount:,.2f}")
        print(f"  Description: Opening Balance")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("CEO Capital System - Database Setup")
    print("=" * 60)
    print()
    
    # Create table
    table_created = add_ceo_capital_table()
    
    if table_created:
        print()
        print("=" * 60)
        print("Set Opening Balance")
        print("=" * 60)
        print()
        print("This will set the initial CEO Capital balance.")
        print("This represents the CEO's available money from business.")
        print()
        
        try:
            amount_str = input("Enter opening balance amount (PKR): ")
            amount = float(amount_str.replace(',', ''))
            
            if amount < 0:
                print("✗ Amount cannot be negative")
                exit(1)
            
            # Get date (optional)
            date_str = input("Enter date (YYYY-MM-DD) or press Enter for first day of current month: ").strip()
            
            print()
            set_opening_balance(amount, date_str if date_str else None)
            
        except ValueError:
            print("✗ Invalid amount entered")
            exit(1)
        except KeyboardInterrupt:
            print("\n✗ Cancelled by user")
            exit(1)
    
    print()
    print("=" * 60)
    print("Setup Complete!")
    print("=" * 60)
    print()
    print("Next steps:")
    print("1. Restart backend server")
    print("2. View CEO Capital in Dashboard")
    print("3. Start tracking transactions")

"""
Set opening balance for office expenses
This script adds an opening balance entry from profit allocation
"""

from database import SessionLocal
from models import OfficeExpense
from datetime import date

def set_opening_balance(amount: float, opening_date: str = None):
    """
    Set opening balance for office expenses
    
    Args:
        amount: Opening balance amount (from profit allocation)
        opening_date: Date for opening balance (format: YYYY-MM-DD), defaults to first day of current month
    """
    db = SessionLocal()
    
    try:
        # Use provided date or first day of current month
        if opening_date:
            balance_date = date.fromisoformat(opening_date)
        else:
            today = date.today()
            balance_date = date(today.year, today.month, 1)
        
        # Check if opening balance already exists for this month
        existing = db.query(OfficeExpense).filter(
            OfficeExpense.date == balance_date,
            OfficeExpense.account_title == "OPENING BALANCE"
        ).first()
        
        if existing:
            print(f"✗ Opening balance already exists for {balance_date}")
            print(f"  Current amount: PKR {existing.amount_received:,.2f}")
            
            update = input("\nDo you want to update it? (yes/no): ").lower()
            if update == 'yes':
                existing.amount_received = amount
                db.commit()
                print(f"✓ Opening balance updated to PKR {amount:,.2f}")
            else:
                print("✗ No changes made")
            return
        
        # Create opening balance entry
        opening_balance = OfficeExpense(
            date=balance_date,
            entry_type='cash_received',
            account_title='OPENING BALANCE',
            particulars='Opening Balance for Office Expenses (Allocated from Profit)',
            amount_received=amount,
            amount_paid=0.0,
            created_by=1  # Admin user
        )
        
        db.add(opening_balance)
        db.commit()
        
        print(f"✓ Opening balance set successfully!")
        print(f"  Date: {balance_date}")
        print(f"  Amount: PKR {amount:,.2f}")
        print(f"  Description: Allocated from Profit")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Set Office Expenses Opening Balance")
    print("=" * 60)
    print()
    print("This will add an opening balance entry for office expenses.")
    print("The amount should come from profit allocation.")
    print()
    
    # Get amount from user
    try:
        amount_str = input("Enter opening balance amount (PKR): ")
        amount = float(amount_str.replace(',', ''))
        
        if amount <= 0:
            print("✗ Amount must be greater than 0")
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

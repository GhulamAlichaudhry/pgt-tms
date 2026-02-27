"""
Fix Payables Outstanding Amount - Set NULL values to amount
"""
from database import SessionLocal
from sqlalchemy import text

def fix_payables_outstanding():
    """Set outstanding_amount = amount where outstanding_amount is NULL"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print("  FIXING PAYABLES OUTSTANDING AMOUNT")
        print("=" * 70)
        
        # Count payables with NULL outstanding_amount
        result = db.execute(text("SELECT COUNT(*) FROM payables WHERE outstanding_amount IS NULL"))
        null_count = result.scalar()
        print(f"\n📋 Payables with NULL outstanding_amount: {null_count}")
        
        if null_count > 0:
            # Update NULL outstanding_amount to equal amount
            query = text("UPDATE payables SET outstanding_amount = amount WHERE outstanding_amount IS NULL")
            db.execute(query)
            db.commit()
            print(f"✅ Updated {null_count} payables")
        else:
            print("✅ No payables need updating")
        
        # Verify the update
        result = db.execute(text("SELECT COUNT(*) FROM payables WHERE outstanding_amount IS NULL"))
        remaining_null = result.scalar()
        print(f"\n📊 Payables with NULL outstanding_amount after fix: {remaining_null}")
        
        # Show summary
        result = db.execute(text("""
            SELECT 
                COUNT(*) as total,
                SUM(amount) as total_amount,
                SUM(outstanding_amount) as total_outstanding
            FROM payables
        """))
        row = result.fetchone()
        print(f"\n📊 Payables Summary:")
        print(f"   Total payables: {row[0]}")
        print(f"   Total amount: PKR {row[1]:,.2f}" if row[1] else "   Total amount: PKR 0.00")
        print(f"   Total outstanding: PKR {row[2]:,.2f}" if row[2] else "   Total outstanding: PKR 0.00")
        
        print("\n" + "=" * 70)
        print("  FIX COMPLETE! ✅")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_payables_outstanding()

"""
Recreate Cash Transactions Table with Correct Structure
"""
from database import SessionLocal, engine
from sqlalchemy import text
import models

def recreate_cash_transactions():
    """Drop old cash_transactions table and create new one"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print("  RECREATING CASH_TRANSACTIONS TABLE")
        print("=" * 70)
        
        # Drop the old table
        print("\n📋 Dropping old cash_transactions table...")
        db.execute(text("DROP TABLE IF EXISTS cash_transactions"))
        db.commit()
        print("✅ Old table dropped")
        
        # Create the new table with correct structure
        print("\n📋 Creating new cash_transactions table...")
        models.Base.metadata.tables['cash_transactions'].create(engine)
        print("✅ New table created")
        
        # Verify the new structure
        from sqlalchemy import inspect
        inspector = inspect(engine)
        columns = [c['name'] for c in inspector.get_columns('cash_transactions')]
        print(f"\n📊 New table columns: {columns}")
        
        print("\n" + "=" * 70)
        print("  TABLE RECREATION COMPLETE! ✅")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    recreate_cash_transactions()

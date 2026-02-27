"""
Add CEO Capital Transaction ID link to Office Expenses table
"""
from sqlalchemy import create_engine, text
import os

SQLALCHEMY_DATABASE_URL = "sqlite:///./pgt_tms.db"

def add_ceo_capital_link():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("PRAGMA table_info(office_expenses)"))
        columns = [row[1] for row in result]
        
        if 'ceo_capital_transaction_id' not in columns:
            print("Adding ceo_capital_transaction_id column to office_expenses table...")
            conn.execute(text("""
                ALTER TABLE office_expenses 
                ADD COLUMN ceo_capital_transaction_id INTEGER
            """))
            conn.commit()
            print("✅ Column added successfully!")
        else:
            print("✓ Column already exists")

if __name__ == "__main__":
    print("=" * 60)
    print("Office Expenses - CEO Capital Link Migration")
    print("=" * 60)
    add_ceo_capital_link()
    print("\n✅ Migration complete!")

"""
Add Staff Advance Ledger System - Director's Rule #1
Smart tracking of staff advances with complete history
"""
from sqlalchemy import create_engine, text, Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./pgt_tms.db"

def add_staff_advance_ledger():
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    
    with engine.connect() as conn:
        # Check if table exists
        result = conn.execute(text("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name='staff_advance_ledger'
        """))
        
        if not result.fetchone():
            print("Creating staff_advance_ledger table...")
            conn.execute(text("""
                CREATE TABLE staff_advance_ledger (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    staff_id INTEGER NOT NULL,
                    transaction_date DATETIME NOT NULL,
                    transaction_type VARCHAR NOT NULL,
                    amount FLOAT NOT NULL,
                    balance_after FLOAT NOT NULL,
                    description TEXT,
                    payroll_id INTEGER,
                    created_by INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (staff_id) REFERENCES staff(id),
                    FOREIGN KEY (payroll_id) REFERENCES payroll_entries(id),
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            """))
            conn.commit()
            print("✅ staff_advance_ledger table created!")
        else:
            print("✓ staff_advance_ledger table already exists")
        
        # Add recovery_start_date to staff table if not exists
        result = conn.execute(text("PRAGMA table_info(staff)"))
        columns = [row[1] for row in result]
        
        if 'recovery_start_date' not in columns:
            print("Adding recovery_start_date to staff table...")
            conn.execute(text("ALTER TABLE staff ADD COLUMN recovery_start_date DATE"))
            conn.commit()
            print("✅ recovery_start_date added!")
        
        if 'advance_given_date' not in columns:
            print("Adding advance_given_date to staff table...")
            conn.execute(text("ALTER TABLE staff ADD COLUMN advance_given_date DATE"))
            conn.commit()
            print("✅ advance_given_date added!")

if __name__ == "__main__":
    print("=" * 60)
    print("Staff Advance Ledger System - Setup")
    print("Director's Rule #1: Smart Recovery Tracking")
    print("=" * 60)
    add_staff_advance_ledger()
    print("\n✅ Setup complete!")
    print("\nNext: Run payroll to see automatic recovery deductions")

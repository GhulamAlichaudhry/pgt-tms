"""
Migration: Add recovery_start_date and advance_given_date to staff table
Director's Rule #1: Staff Advance Recovery System
"""

from sqlalchemy import create_engine, text
from database import DATABASE_URL

def migrate():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if columns exist
        result = conn.execute(text("PRAGMA table_info(staff)"))
        columns = [row[1] for row in result.fetchall()]
        
        # Add recovery_start_date if not exists
        if 'recovery_start_date' not in columns:
            print("Adding recovery_start_date column...")
            conn.execute(text("""
                ALTER TABLE staff 
                ADD COLUMN recovery_start_date TIMESTAMP
            """))
            conn.commit()
            print("✅ recovery_start_date column added")
        else:
            print("✅ recovery_start_date column already exists")
        
        # Add advance_given_date if not exists
        if 'advance_given_date' not in columns:
            print("Adding advance_given_date column...")
            conn.execute(text("""
                ALTER TABLE staff 
                ADD COLUMN advance_given_date TIMESTAMP
            """))
            conn.commit()
            print("✅ advance_given_date column added")
        else:
            print("✅ advance_given_date column already exists")
        
        print("\n✅ Migration complete!")
        print("Staff table now supports:")
        print("  - recovery_start_date: When recovery schedule started")
        print("  - advance_given_date: When advance was given")

if __name__ == "__main__":
    migrate()

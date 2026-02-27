#!/usr/bin/env python3
"""
Migration Script: Add local_shifting_charges field to trips table
"""

from sqlalchemy import create_engine, text
from database import DATABASE_URL

def migrate():
    """Add local_shifting_charges column to trips table"""
    engine = create_engine(DATABASE_URL)
    
    print("=" * 60)
    print("  Adding local_shifting_charges field to trips table")
    print("=" * 60)
    
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("PRAGMA table_info(trips)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'local_shifting_charges' in columns:
                print("✅ Column 'local_shifting_charges' already exists!")
                return
            
            # Add the column
            print("\n📝 Adding local_shifting_charges column...")
            conn.execute(text("""
                ALTER TABLE trips 
                ADD COLUMN local_shifting_charges FLOAT DEFAULT 0.0
            """))
            conn.commit()
            
            print("✅ Column added successfully!")
            
            # Update existing trips to recalculate profit
            print("\n📝 Updating existing trips...")
            result = conn.execute(text("SELECT COUNT(*) FROM trips"))
            trip_count = result.fetchone()[0]
            
            if trip_count > 0:
                # Recalculate gross_profit for existing trips
                # gross_profit = client_freight - (vendor_freight + local_shifting_charges)
                conn.execute(text("""
                    UPDATE trips 
                    SET gross_profit = client_freight - (vendor_freight + COALESCE(local_shifting_charges, 0))
                """))
                
                # Recalculate net_profit
                # net_profit = gross_profit - (advance_paid + fuel_cost + munshiyana_bank_charges + other_expenses)
                conn.execute(text("""
                    UPDATE trips 
                    SET net_profit = gross_profit - (
                        COALESCE(advance_paid, 0) + 
                        COALESCE(fuel_cost, 0) + 
                        COALESCE(munshiyana_bank_charges, 0) + 
                        COALESCE(other_expenses, 0)
                    )
                """))
                
                # Recalculate profit_margin
                conn.execute(text("""
                    UPDATE trips 
                    SET profit_margin = CASE 
                        WHEN client_freight > 0 THEN (net_profit / client_freight) * 100
                        ELSE 0
                    END
                """))
                
                conn.commit()
                print(f"✅ Updated {trip_count} existing trips with recalculated profits!")
            
            print("\n" + "=" * 60)
            print("✅ Migration completed successfully!")
            print("=" * 60)
            print("\n📋 Summary:")
            print("   - Added 'local_shifting_charges' column to trips table")
            print("   - Default value: 0.0")
            print(f"   - Updated {trip_count} existing trips")
            print("\n💡 Note:")
            print("   - Local + Shifting charges are now added to vendor freight")
            print("   - Total vendor cost = vendor_freight + local_shifting_charges")
            print("   - Profit calculations updated accordingly")
            print("\n")
            
    except Exception as e:
        print(f"\n❌ Error during migration: {e}")
        raise

if __name__ == "__main__":
    migrate()

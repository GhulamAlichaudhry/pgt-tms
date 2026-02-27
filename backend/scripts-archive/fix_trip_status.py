"""
Fix Trip Status - Convert old status values to new TripStatus enum
"""
from database import SessionLocal, engine
from sqlalchemy import text

def fix_trip_status():
    """Convert old trip status values to new TripStatus enum values"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 70)
        print("  FIXING TRIP STATUS VALUES")
        print("=" * 70)
        
        # Get all unique status values
        result = db.execute(text("SELECT DISTINCT status FROM trips"))
        current_statuses = [row[0] for row in result]
        print(f"\n📋 Current status values in database: {current_statuses}")
        
        # Mapping from old values to new enum values
        status_mapping = {
            'pending': 'DRAFT',
            'in_progress': 'ACTIVE',
            'completed': 'COMPLETED',
            'cancelled': 'DRAFT',  # Map cancelled to DRAFT
            None: 'DRAFT'  # Map NULL to DRAFT
        }
        
        # Update each old status to new enum value
        for old_status, new_status in status_mapping.items():
            if old_status in current_statuses or old_status is None:
                if old_status is None:
                    query = text("UPDATE trips SET status = :new_status WHERE status IS NULL")
                else:
                    query = text("UPDATE trips SET status = :new_status WHERE status = :old_status")
                    db.execute(query, {"old_status": old_status, "new_status": new_status})
                    print(f"✅ Updated '{old_status}' → '{new_status}'")
                
                db.commit()
        
        # Verify the update
        result = db.execute(text("SELECT DISTINCT status FROM trips"))
        new_statuses = [row[0] for row in result]
        print(f"\n📋 New status values in database: {new_statuses}")
        
        # Count trips by status
        result = db.execute(text("SELECT status, COUNT(*) FROM trips GROUP BY status"))
        print(f"\n📊 Trip counts by status:")
        for row in result:
            print(f"   {row[0]}: {row[1]} trips")
        
        print("\n" + "=" * 70)
        print("  STATUS FIX COMPLETE! ✅")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    fix_trip_status()

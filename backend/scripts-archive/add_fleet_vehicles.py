#!/usr/bin/env python3
"""
Add Fleet Vehicles to Database
Adds all vehicles from your fleet list
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def add_fleet_vehicles():
    """Add all vehicles from the fleet"""
    db = SessionLocal()
    
    try:
        # Your fleet vehicles with types
        fleet_vehicles = [
            # 40 Ft Containers (13 vehicles)
            {"vehicle_no": "PGT-40C-001", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-002", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-003", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-004", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-005", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-006", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-007", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-008", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-009", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-010", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-011", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-012", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            {"vehicle_no": "PGT-40C-013", "vehicle_type": "40 Ft Container", "capacity_tons": 28},
            
            # Flat Beds (8 vehicles)
            {"vehicle_no": "PGT-FB-001", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            {"vehicle_no": "PGT-FB-002", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            {"vehicle_no": "PGT-FB-003", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            {"vehicle_no": "PGT-FB-004", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            {"vehicle_no": "PGT-FB-005", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            {"vehicle_no": "PGT-FB-006", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            {"vehicle_no": "PGT-FB-007", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            {"vehicle_no": "PGT-FB-008", "vehicle_type": "Flat Bed", "capacity_tons": 25},
            
            # 20 Ft Container (1 vehicle)
            {"vehicle_no": "PGT-20C-001", "vehicle_type": "20 Ft Container", "capacity_tons": 22},
        ]
        
        added_count = 0
        skipped_count = 0
        
        print("\n📋 Adding Fleet Vehicles:")
        print("="*60)
        
        for vehicle_data in fleet_vehicles:
            # Check if vehicle already exists
            existing = db.query(models.Vehicle).filter(
                models.Vehicle.vehicle_no == vehicle_data["vehicle_no"]
            ).first()
            
            if existing:
                print(f"⏭️  {vehicle_data['vehicle_no']} - {vehicle_data['vehicle_type']} (exists)")
                skipped_count += 1
                continue
            
            # Add vehicle
            vehicle = models.Vehicle(
                vehicle_no=vehicle_data["vehicle_no"],
                vehicle_type=vehicle_data["vehicle_type"],
                capacity_tons=vehicle_data["capacity_tons"]
            )
            
            db.add(vehicle)
            print(f"✅ {vehicle_data['vehicle_no']} - {vehicle_data['vehicle_type']} ({vehicle_data['capacity_tons']}T)")
            added_count += 1
        
        db.commit()
        
        print("\n" + "="*60)
        print(f"📊 Summary:")
        print(f"   ✅ Added: {added_count} vehicles")
        print(f"   ⏭️  Skipped: {skipped_count} vehicles (already exist)")
        print(f"   📝 Total vehicles in list: {len(fleet_vehicles)}")
        print("="*60)
        
        # Show breakdown by type
        print("\n📈 Fleet Breakdown:")
        print(f"   🚛 40 Ft Containers: 13 vehicles (28 tons each)")
        print(f"   🚚 Flat Beds: 8 vehicles (25 tons each)")
        print(f"   📦 20 Ft Container: 1 vehicle (22 tons)")
        print(f"   📊 Total Fleet: 22 vehicles")
        print(f"   💪 Total Capacity: {(13*28) + (8*25) + (1*22)} tons")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Adding PGT Fleet Vehicles to Database...")
    print("="*60)
    success = add_fleet_vehicles()
    
    if success:
        print("\n✅ Fleet vehicles added successfully!")
        print("\nℹ️  Note:")
        print("   - Vehicle numbers are auto-generated (PGT-40C-001, PGT-FB-001, etc.)")
        print("   - You can edit vehicle numbers in Settings page")
        print("   - All vehicles are now available in Fleet Operations dropdown")
        print("\n💡 Next Steps:")
        print("   1. Go to Settings → Vehicles")
        print("   2. Update vehicle numbers with actual registration numbers")
        print("   3. Add any additional vehicle details")
    else:
        print("\n❌ Failed to add vehicles. Please check the error above.")

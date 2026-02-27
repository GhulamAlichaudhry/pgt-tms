#!/usr/bin/env python3
"""
Add Common Vendors/Brokers to Database
Adds frequently used vendors to make data entry faster
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def add_common_vendors():
    """Add common vendors/brokers used in operations"""
    db = SessionLocal()
    
    try:
        # List of common vendors (unique names only)
        common_vendors = [
            "Akram",
            "Shahi Cargo",
            "Adnan Fakhr e Sahiwal",
            "Haji Azhar",
            "Afzal AB",
            "baba Fareed",
            "Shafa Ullah",
            "Anas Bajwa",
            "Jam Farhan",
            "Bilawal Shakeel Goods",
            "Umair Haroon",
            "Farooq",
            "Nabeel",
            "Doran",
            "Ajmal",
            "Mushtaq Super",
            "Jam",
            "Shafa Ulah",
            "Ramzan Dar",
            "Shafaullah",
            "Amir",
            "Roshan"
        ]
        
        # Remove duplicates and sort
        unique_vendors = sorted(list(set(common_vendors)))
        
        added_count = 0
        skipped_count = 0
        
        for vendor_name in unique_vendors:
            # Check if vendor already exists
            existing = db.query(models.Vendor).filter(
                models.Vendor.name == vendor_name
            ).first()
            
            if existing:
                print(f"⏭️  Skipped: {vendor_name} (already exists)")
                skipped_count += 1
                continue
            
            # Create vendor code from name
            vendor_code = vendor_name.upper().replace(" ", "_")[:10]
            
            # Add vendor
            vendor = models.Vendor(
                name=vendor_name,
                vendor_code=vendor_code,
                contact_person="",
                phone="",
                email="",
                address=""
            )
            
            db.add(vendor)
            print(f"✅ Added: {vendor_name}")
            added_count += 1
        
        db.commit()
        
        print("\n" + "="*50)
        print(f"📊 Summary:")
        print(f"   ✅ Added: {added_count} vendors")
        print(f"   ⏭️  Skipped: {skipped_count} vendors (already exist)")
        print(f"   📝 Total unique vendors: {len(unique_vendors)}")
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Adding Common Vendors/Brokers to Database...")
    print("="*50)
    success = add_common_vendors()
    
    if success:
        print("\n✅ Common vendors added successfully!")
        print("\nℹ️  Note: You can still add new vendors manually from the Settings page.")
    else:
        print("\n❌ Failed to add vendors. Please check the error above.")

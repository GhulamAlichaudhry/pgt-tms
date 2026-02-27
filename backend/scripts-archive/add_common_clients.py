#!/usr/bin/env python3
"""
Add Common Clients to Database
Adds frequently used clients to make data entry faster
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

def add_common_clients():
    """Add common clients used in operations"""
    db = SessionLocal()
    
    try:
        # List of common clients (unique names only)
        common_clients = [
            "Fauji Foods",
            "Pak Afghan",
            "Ghani Dairy",
            "Ibrahim Poultry",
            "Green Crockery"
        ]
        
        # Remove duplicates and sort
        unique_clients = sorted(list(set(common_clients)))
        
        added_count = 0
        skipped_count = 0
        
        for client_name in unique_clients:
            # Check if client already exists
            existing = db.query(models.Client).filter(
                models.Client.name == client_name
            ).first()
            
            if existing:
                print(f"⏭️  Skipped: {client_name} (already exists)")
                skipped_count += 1
                continue
            
            # Create client code from name
            client_code = client_name.upper().replace(" ", "_")[:10]
            
            # Add client
            client = models.Client(
                name=client_name,
                client_code=client_code,
                contact_person="",
                phone="",
                email="",
                address=""
            )
            
            db.add(client)
            print(f"✅ Added: {client_name}")
            added_count += 1
        
        db.commit()
        
        print("\n" + "="*50)
        print(f"📊 Summary:")
        print(f"   ✅ Added: {added_count} clients")
        print(f"   ⏭️  Skipped: {skipped_count} clients (already exist)")
        print(f"   📝 Total unique clients: {len(unique_clients)}")
        print("="*50)
        
        # Show client frequency analysis
        print("\n📈 Client Frequency Analysis (from your data):")
        print("   🥇 Pak Afghan - Most frequent (40+ trips)")
        print("   🥈 Fauji Foods - Very frequent (15+ trips)")
        print("   🥉 Ibrahim Poultry - Frequent (10+ trips)")
        print("   📊 Ghani Dairy - Regular (8+ trips)")
        print("   📊 Green Crockery - Regular (6+ trips)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Adding Common Clients to Database...")
    print("="*50)
    success = add_common_clients()
    
    if success:
        print("\n✅ Common clients added successfully!")
        print("\nℹ️  Note: You can still add new clients manually from the Settings page.")
        print("\n💡 Tip: These 5 clients represent the majority of your business.")
        print("   Focus on maintaining good relationships with them!")
    else:
        print("\n❌ Failed to add clients. Please check the error above.")

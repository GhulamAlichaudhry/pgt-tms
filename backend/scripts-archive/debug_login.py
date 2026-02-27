#!/usr/bin/env python3
"""
Debug script to check login authentication
"""

from sqlalchemy.orm import Session
from database import SessionLocal
import models
from auth import get_password_hash, verify_password

def debug_login():
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("DEBUG: Checking Admin User in Database")
        print("="*60)
        
        # Get admin user
        admin = db.query(models.User).filter(models.User.username == "admin").first()
        
        if not admin:
            print("❌ ERROR: Admin user does not exist in database!")
            return
        
        print(f"✅ Admin user found:")
        print(f"   ID: {admin.id}")
        print(f"   Username: {admin.username}")
        print(f"   Email: {admin.email}")
        print(f"   Full Name: {admin.full_name}")
        print(f"   Role: {admin.role}")
        print(f"   Is Active: {admin.is_active}")
        print(f"   Hashed Password: {admin.hashed_password[:50]}...")
        
        # Test password verification
        print("\n" + "="*60)
        print("Testing Password Verification")
        print("="*60)
        
        test_password = "admin123"
        print(f"Testing password: '{test_password}'")
        
        is_valid = verify_password(test_password, admin.hashed_password)
        print(f"Password verification result: {is_valid}")
        
        if is_valid:
            print("✅ Password 'admin123' is CORRECT")
        else:
            print("❌ Password 'admin123' is INCORRECT")
            print("\nGenerating new hash for 'admin123'...")
            new_hash = get_password_hash("admin123")
            print(f"New hash: {new_hash[:50]}...")
            
            # Update the password
            admin.hashed_password = new_hash
            db.commit()
            print("✅ Password updated in database")
            
            # Verify again
            is_valid_now = verify_password(test_password, admin.hashed_password)
            print(f"Verification after update: {is_valid_now}")
        
        print("\n" + "="*60)
        print("All Users in Database:")
        print("="*60)
        
        all_users = db.query(models.User).all()
        for user in all_users:
            print(f"- {user.username} ({user.role}) - Active: {user.is_active}")
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_login()

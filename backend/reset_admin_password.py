#!/usr/bin/env python3
"""
Script to reset admin password
Run this if you forgot the admin password or need to reset it
"""

from sqlalchemy.orm import Session
from database import SessionLocal
import models
from auth import get_password_hash

def reset_admin_password(new_password: str = "admin123"):
    """Reset admin password to default or specified password"""
    
    db = SessionLocal()
    
    try:
        # Find admin user
        admin_user = db.query(models.User).filter(models.User.username == "admin").first()
        
        if not admin_user:
            print("❌ Admin user not found!")
            print("Creating admin user...")
            
            # Create admin user
            admin_user = models.User(
                username="admin",
                email="admin@pgt.com",
                hashed_password=get_password_hash(new_password),
                full_name="PGT Administrator",
                role=models.UserRole.ADMIN,
                is_active=True
            )
            
            db.add(admin_user)
            db.commit()
            
            print("✅ Admin user created successfully!")
            print(f"   Username: admin")
            print(f"   Password: {new_password}")
            return
        
        # Reset password
        admin_user.hashed_password = get_password_hash(new_password)
        admin_user.is_active = True  # Ensure user is active
        db.commit()
        
        print("✅ Admin password reset successfully!")
        print(f"   Username: admin")
        print(f"   Password: {new_password}")
        print(f"   Email: {admin_user.email}")
        print(f"   Role: {admin_user.role.value}")
        print(f"   Status: {'Active' if admin_user.is_active else 'Inactive'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 60)
    print("Reset Admin Password")
    print("=" * 60)
    print()
    
    # Ask for new password or use default
    choice = input("Use default password 'admin123'? (yes/no): ").lower().strip()
    
    if choice == 'yes' or choice == 'y' or choice == '':
        reset_admin_password("admin123")
    else:
        new_pass = input("Enter new password: ").strip()
        if len(new_pass) < 6:
            print("❌ Password must be at least 6 characters!")
        else:
            reset_admin_password(new_pass)
    
    print()
    print("=" * 60)
    print("You can now login with the credentials above")
    print("=" * 60)

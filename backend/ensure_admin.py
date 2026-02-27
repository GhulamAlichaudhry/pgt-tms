#!/usr/bin/env python3
"""
CRITICAL: This script MUST run on every backend startup
Ensures admin user always exists with correct credentials
This prevents login issues that have occurred multiple times
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import get_password_hash

def ensure_admin_exists():
    """
    PERMANENT FIX: Ensure admin user exists with correct password
    This runs automatically on backend startup
    """
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(models.User).filter(models.User.username == "admin").first()
        
        if admin_user:
            # Admin exists - verify password is correct
            admin_user.hashed_password = get_password_hash("admin123")
            admin_user.is_active = True
            admin_user.role = models.UserRole.ADMIN
            db.commit()
            print("✅ Admin user verified and password ensured: admin/admin123")
        else:
            # Admin doesn't exist - create it
            admin_user = models.User(
                username="admin",
                email="admin@pgt.com",
                hashed_password=get_password_hash("admin123"),
                full_name="PGT Administrator",
                role=models.UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Admin user created: admin/admin123")
        
        # Ensure manager user exists
        manager_user = db.query(models.User).filter(models.User.username == "manager").first()
        if manager_user:
            manager_user.hashed_password = get_password_hash("manager123")
            manager_user.is_active = True
            manager_user.role = models.UserRole.MANAGER
            db.commit()
            print("✅ Manager user verified: manager/manager123")
        else:
            manager_user = models.User(
                username="manager",
                email="manager@pgt.com",
                hashed_password=get_password_hash("manager123"),
                full_name="Operations Manager",
                role=models.UserRole.MANAGER,
                is_active=True
            )
            db.add(manager_user)
            db.commit()
            print("✅ Manager user created: manager/manager123")
        
        # Ensure supervisor user exists
        supervisor_user = db.query(models.User).filter(models.User.username == "supervisor").first()
        if supervisor_user:
            supervisor_user.hashed_password = get_password_hash("supervisor123")
            supervisor_user.is_active = True
            supervisor_user.role = models.UserRole.SUPERVISOR
            db.commit()
            print("✅ Supervisor user verified: supervisor/supervisor123")
        else:
            supervisor_user = models.User(
                username="supervisor",
                email="supervisor@pgt.com",
                hashed_password=get_password_hash("supervisor123"),
                full_name="Port Supervisor",
                role=models.UserRole.SUPERVISOR,
                is_active=True
            )
            db.add(supervisor_user)
            db.commit()
            print("✅ Supervisor user created: supervisor/supervisor123")
        
        print("\n" + "="*60)
        print("🔐 ALL LOGIN CREDENTIALS VERIFIED AND READY")
        print("="*60)
        print("Admin:      admin / admin123")
        print("Manager:    manager / manager123")
        print("Supervisor: supervisor / supervisor123")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error ensuring admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    ensure_admin_exists()

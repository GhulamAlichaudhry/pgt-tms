#!/usr/bin/env python3
"""
Script to create an admin user for PGT International Smart TMS
Run this after setting up the database to create the initial admin user.
"""

from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import get_password_hash

def create_admin_user():
    # Create database tables
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(models.User).filter(models.User.username == "admin").first()
        if existing_admin:
            print("Admin user already exists!")
            return
        
        # Create admin user
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
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        print("Please change the password after first login.")
        
        # Create some sample data
        create_sample_data(db)
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

def create_sample_data(db: Session):
    """Create some sample data for demonstration"""
    
    # Sample vehicles
    vehicles = [
        models.Vehicle(vehicle_no="PGT-001", vehicle_type="Truck", capacity_tons=20.0),
        models.Vehicle(vehicle_no="PGT-002", vehicle_type="Trailer", capacity_tons=40.0),
        models.Vehicle(vehicle_no="PGT-003", vehicle_type="Truck", capacity_tons=15.0),
    ]
    
    for vehicle in vehicles:
        existing = db.query(models.Vehicle).filter(models.Vehicle.vehicle_no == vehicle.vehicle_no).first()
        if not existing:
            db.add(vehicle)
    
    # Sample staff
    staff_members = [
        models.Staff(
            employee_id="EMP001",
            name="Muhammad Ali",
            position="Port Supervisor",
            gross_salary=45000.0,
            advance_balance=0.0,
            monthly_deduction=0.0
        ),
        models.Staff(
            employee_id="EMP002",
            name="Waqar Sajid",
            position="Operational Manager",
            gross_salary=65000.0,
            advance_balance=140000.0,
            monthly_deduction=15000.0
        ),
        models.Staff(
            employee_id="EMP003",
            name="Muhammad Hussain",
            position="Accounts Manager",
            gross_salary=55000.0,
            advance_balance=140000.0,
            monthly_deduction=12000.0
        ),
    ]
    
    for staff in staff_members:
        existing = db.query(models.Staff).filter(models.Staff.employee_id == staff.employee_id).first()
        if not existing:
            db.add(staff)
    
    # Sample vendor
    vendor = models.Vendor(
        name="Pak Afghan Logistics",
        contact_person="Ahmed Khan",
        phone="+92 300 1234567",
        email="contact@pakafghan.com",
        address="Karachi Port, Pakistan",
        current_balance=4928445.0
    )
    
    existing_vendor = db.query(models.Vendor).filter(models.Vendor.name == vendor.name).first()
    if not existing_vendor:
        db.add(vendor)
    
    db.commit()
    print("Sample data created successfully!")

if __name__ == "__main__":
    create_admin_user()
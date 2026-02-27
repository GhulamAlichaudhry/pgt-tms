#!/usr/bin/env python3
"""
Initialize the PGT TMS database with correct schema and sample data
"""

import sys
import traceback
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from auth import get_password_hash

def init_database():
    """Initialize database with correct schema"""
    try:
        print("Creating database tables...")
        # Drop all tables and recreate them
        models.Base.metadata.drop_all(bind=engine)
        models.Base.metadata.create_all(bind=engine)
        print("✓ Database tables created successfully")
        
        # Create admin user
        create_admin_user()
        
        # Create sample data
        create_sample_data()
        
        print("\n" + "="*50)
        print("Database initialization complete!")
        print("Login credentials: admin / admin123")
        print("="*50)
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        traceback.print_exc()
        sys.exit(1)

def create_admin_user():
    """Create admin user"""
    db = SessionLocal()
    
    try:
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
        print("✓ Admin user created")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_sample_data():
    """Create sample data"""
    db = SessionLocal()
    
    try:
        # Get the admin user (created in previous step)
        admin_user = db.query(models.User).filter(models.User.username == "admin").first()
        if not admin_user:
            raise Exception("Admin user not found. Please create admin user first.")
        
        # Sample vehicles
        vehicles = [
            models.Vehicle(vehicle_no="KHI-1234", vehicle_type="Container Truck", capacity_tons=20.0),
            models.Vehicle(vehicle_no="KHI-5678", vehicle_type="Container Truck", capacity_tons=25.0),
            models.Vehicle(vehicle_no="KHI-9012", vehicle_type="Trailer", capacity_tons=30.0),
            models.Vehicle(vehicle_no="LHR-3456", vehicle_type="Container Truck", capacity_tons=22.0),
            models.Vehicle(vehicle_no="ISB-7890", vehicle_type="Pickup", capacity_tons=2.0),
        ]
        
        for vehicle in vehicles:
            db.add(vehicle)
        
        # Sample staff
        staff_members = [
            models.Staff(
                employee_id="EMP001",
                name="Muhammad Ali",
                position="Port Supervisor",
                gross_salary=45000.0,
                advance_balance=25000.0,
                monthly_deduction=5000.0
            ),
            models.Staff(
                employee_id="EMP002", 
                name="Waqar Sajid",
                position="Operations Manager",
                gross_salary=75000.0,
                advance_balance=50000.0,
                monthly_deduction=10000.0
            ),
            models.Staff(
                employee_id="EMP003",
                name="Muhammad Hussain",
                position="Accounts Manager", 
                gross_salary=60000.0,
                advance_balance=140000.0,
                monthly_deduction=15000.0
            ),
            models.Staff(
                employee_id="EMP004",
                name="Ahmed Khan",
                position="Driver",
                gross_salary=35000.0,
                advance_balance=15000.0,
                monthly_deduction=3000.0
            )
        ]
        
        for staff in staff_members:
            db.add(staff)
        
        # Sample vendors
        vendors = [
            models.Vendor(
                name="Pak Afghan Logistics",
                contact_person="Akram Shah",
                phone="+92-300-1234567",
                email="info@pakafghan.com",
                address="Karachi Port Area",
                current_balance=2500000.0
            ),
            models.Vendor(
                name="Fazal Foods",
                contact_person="Fazal Ahmed",
                phone="+92-321-9876543", 
                email="contact@fazalfoods.com",
                address="Industrial Area, Karachi",
                current_balance=1800000.0
            ),
            models.Vendor(
                name="Shahid Ilyas Transport",
                contact_person="Shahid Ilyas",
                phone="+92-333-5555555",
                email="shahid@transport.com", 
                address="Transport Hub, Lahore",
                current_balance=628445.0
            )
        ]
        
        for vendor in vendors:
            db.add(vendor)
        
        # Sample expenses (all created by admin user)
        expenses = [
            models.Expense(
                date=datetime.now() - timedelta(days=5),
                expense_category="fuel",
                description="Diesel fuel for KHI-1234",
                amount=15000.0,
                vehicle_id=1,
                created_by=admin_user.id
            ),
            models.Expense(
                date=datetime.now() - timedelta(days=3),
                expense_category="maintenance",
                description="Oil change and filter replacement",
                amount=8500.0,
                vehicle_id=2,
                created_by=admin_user.id
            ),
            models.Expense(
                date=datetime.now() - timedelta(days=2),
                expense_category="office",
                description="Office supplies and stationery",
                amount=3200.0,
                created_by=admin_user.id
            ),
            models.Expense(
                date=datetime.now() - timedelta(days=1),
                expense_category="tolls",
                description="Highway tolls - Karachi to Lahore",
                amount=2500.0,
                vehicle_id=1,
                created_by=admin_user.id
            ),
            models.Expense(
                date=datetime.now(),
                expense_category="repairs",
                description="Brake pad replacement",
                amount=12000.0,
                vehicle_id=3,
                created_by=admin_user.id
            )
        ]
        
        for expense in expenses:
            db.add(expense)

        # Sample payables
        payables = [
            models.Payable(
                vendor_id=1,
                invoice_number="INV-2024-001",
                description="Transportation services - January",
                amount=250000.0,
                due_date=datetime.now() + timedelta(days=15),
                status="pending"
            ),
            models.Payable(
                vendor_id=2,
                invoice_number="INV-2024-002",
                description="Fuel supply - December",
                amount=180000.0,
                due_date=datetime.now() + timedelta(days=7),
                status="approved"
            ),
            models.Payable(
                vendor_id=3,
                invoice_number="INV-2024-003",
                description="Vehicle maintenance services",
                amount=85000.0,
                due_date=datetime.now() - timedelta(days=5),  # Overdue
                status="overdue"
            ),
            models.Payable(
                vendor_id=1,
                invoice_number="INV-2024-004",
                description="Port handling charges",
                amount=125000.0,
                due_date=datetime.now() + timedelta(days=30),
                status="pending"
            ),
        ]
        
        for payable in payables:
            db.add(payable)
        
        db.commit()
        print("✓ Sample data created")
        print(f"  - {len(vehicles)} vehicles")
        print(f"  - {len(staff_members)} staff members")
        print(f"  - {len(vendors)} vendors")
        print(f"  - {len(expenses)} sample expenses")
        print(f"  - {len(payables)} sample payables")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
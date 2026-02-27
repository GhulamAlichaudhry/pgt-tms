#!/usr/bin/env python3
"""
Script to add default data to the PGT TMS database
"""

import sys
import traceback
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud
import schemas

# Create database tables
models.Base.metadata.create_all(bind=engine)

def add_default_vehicles():
    """Add default vehicles to the database"""
    db = SessionLocal()
    
    try:
        # Check if vehicles already exist
        existing_vehicles = db.query(models.Vehicle).count()
        if existing_vehicles > 0:
            print(f"Found {existing_vehicles} existing vehicles. Skipping vehicle creation.")
            return
        
        # Default vehicles based on typical PGT International fleet
        default_vehicles = [
            {
                "vehicle_no": "KHI-1234",
                "vehicle_type": "Container Truck",
                "capacity_tons": 20.0
            },
            {
                "vehicle_no": "KHI-5678",
                "vehicle_type": "Container Truck", 
                "capacity_tons": 25.0
            },
            {
                "vehicle_no": "KHI-9012",
                "vehicle_type": "Trailer",
                "capacity_tons": 30.0
            },
            {
                "vehicle_no": "LHR-3456",
                "vehicle_type": "Container Truck",
                "capacity_tons": 22.0
            },
            {
                "vehicle_no": "ISB-7890",
                "vehicle_type": "Pickup",
                "capacity_tons": 2.0
            }
        ]
        
        for vehicle_data in default_vehicles:
            try:
                vehicle = schemas.VehicleCreate(**vehicle_data)
                db_vehicle = models.Vehicle(**vehicle_data)
                db.add(db_vehicle)
                db.commit()
                db.refresh(db_vehicle)
                print(f"Created vehicle: {db_vehicle.vehicle_no} - {db_vehicle.vehicle_type}")
            except Exception as e:
                print(f"Error creating vehicle {vehicle_data['vehicle_no']}: {e}")
                db.rollback()
                
    except Exception as e:
        print(f"Error in add_default_vehicles: {e}")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

def add_default_staff():
    """Add default staff members"""
    db = SessionLocal()
    
    try:
        # Check if staff already exist
        existing_staff = db.query(models.Staff).count()
        if existing_staff > 0:
            print(f"Found {existing_staff} existing staff members. Skipping staff creation.")
            return
            
        # Default staff based on the user's requirements
        default_staff = [
            {
                "employee_id": "EMP001",
                "name": "Muhammad Ali",
                "position": "Port Supervisor",
                "gross_salary": 45000.0,
                "advance_balance": 25000.0,
                "monthly_deduction": 5000.0
            },
            {
                "employee_id": "EMP002", 
                "name": "Waqar Sajid",
                "position": "Operations Manager",
                "gross_salary": 75000.0,
                "advance_balance": 50000.0,
                "monthly_deduction": 10000.0
            },
            {
                "employee_id": "EMP003",
                "name": "Muhammad Hussain",
                "position": "Accounts Manager", 
                "gross_salary": 60000.0,
                "advance_balance": 140000.0,
                "monthly_deduction": 15000.0
            },
            {
                "employee_id": "EMP004",
                "name": "Ahmed Khan",
                "position": "Driver",
                "gross_salary": 35000.0,
                "advance_balance": 15000.0,
                "monthly_deduction": 3000.0
            }
        ]
        
        for staff_data in default_staff:
            try:
                db_staff = models.Staff(**staff_data)
                db.add(db_staff)
                db.commit()
                db.refresh(db_staff)
                print(f"Created staff: {db_staff.name} - {db_staff.position}")
            except Exception as e:
                print(f"Error creating staff {staff_data['name']}: {e}")
                db.rollback()
                
    except Exception as e:
        print(f"Error in add_default_staff: {e}")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

def add_default_vendors():
    """Add default vendors"""
    db = SessionLocal()
    
    try:
        # Check if vendors already exist
        existing_vendors = db.query(models.Vendor).count()
        if existing_vendors > 0:
            print(f"Found {existing_vendors} existing vendors. Skipping vendor creation.")
            return
            
        # Default vendors based on the Excel sheet
        default_vendors = [
            {
                "name": "Pak Afghan Logistics",
                "contact_person": "Akram Shah",
                "phone": "+92-300-1234567",
                "email": "info@pakafghan.com",
                "address": "Karachi Port Area",
                "current_balance": 2500000.0
            },
            {
                "name": "Fazal Foods",
                "contact_person": "Fazal Ahmed",
                "phone": "+92-321-9876543", 
                "email": "contact@fazalfoods.com",
                "address": "Industrial Area, Karachi",
                "current_balance": 1800000.0
            },
            {
                "name": "Shahid Ilyas Transport",
                "contact_person": "Shahid Ilyas",
                "phone": "+92-333-5555555",
                "email": "shahid@transport.com", 
                "address": "Transport Hub, Lahore",
                "current_balance": 628445.0
            }
        ]
        
        for vendor_data in default_vendors:
            try:
                db_vendor = models.Vendor(**vendor_data)
                db.add(db_vendor)
                db.commit()
                db.refresh(db_vendor)
                print(f"Created vendor: {db_vendor.name} - Balance: {db_vendor.current_balance}")
            except Exception as e:
                print(f"Error creating vendor {vendor_data['name']}: {e}")
                db.rollback()
                
    except Exception as e:
        print(f"Error in add_default_vendors: {e}")
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    try:
        print("Adding default data to PGT TMS database...")
        print("=" * 50)
        
        print("\n1. Adding default vehicles...")
        add_default_vehicles()
        
        print("\n2. Adding default staff...")
        add_default_staff()
        
        print("\n3. Adding default vendors...")
        add_default_vendors()
        
        print("\n" + "=" * 50)
        print("Default data setup complete!")
        print("You can now use the application with sample data.")
        
    except Exception as e:
        print(f"Fatal error: {e}")
        traceback.print_exc()
        sys.exit(1)
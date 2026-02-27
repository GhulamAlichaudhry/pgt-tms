#!/usr/bin/env python3
"""
Quick script to find IDs for sample PDF generation
Finds Pak Afghan and Muhammad Hussain IDs
"""

from database import SessionLocal
from models import Vendor, Staff, Client

def find_sample_ids():
    db = SessionLocal()
    
    print("\n" + "="*60)
    print("FINDING IDS FOR SAMPLE PDF GENERATION")
    print("="*60 + "\n")
    
    # Find Pak Afghan as Vendor
    print("Searching for Pak Afghan...")
    pak_afghan_vendor = db.query(Vendor).filter(
        Vendor.name.like('%Pak%Afghan%')
    ).first()
    
    if pak_afghan_vendor:
        print(f"✅ Found as VENDOR:")
        print(f"   ID: {pak_afghan_vendor.id}")
        print(f"   Name: {pak_afghan_vendor.name}")
        print(f"   Balance: PKR {pak_afghan_vendor.current_balance:,.2f}")
        print(f"   URL: http://localhost:8002/reports/vendor-ledger-pdf-enhanced/{pak_afghan_vendor.id}")
    else:
        print("❌ Pak Afghan not found as vendor")
    
    print()
    
    # Find Pak Afghan as Client
    pak_afghan_client = db.query(Client).filter(
        Client.name.like('%Pak%Afghan%')
    ).first()
    
    if pak_afghan_client:
        print(f"✅ Found as CLIENT:")
        print(f"   ID: {pak_afghan_client.id}")
        print(f"   Name: {pak_afghan_client.name}")
        print(f"   Balance: PKR {pak_afghan_client.current_balance:,.2f}")
    
    print("\n" + "-"*60 + "\n")
    
    # Find Muhammad Hussain
    print("Searching for Muhammad Hussain...")
    hussain = db.query(Staff).filter(
        Staff.name.like('%Hussain%')
    ).first()
    
    if hussain:
        print(f"✅ Found STAFF MEMBER:")
        print(f"   ID: {hussain.id}")
        print(f"   Name: {hussain.name}")
        print(f"   Employee ID: {hussain.employee_id}")
        print(f"   Position: {hussain.position}")
        print(f"   Advance Balance: PKR {hussain.advance_balance:,.2f}")
        print(f"   Monthly Deduction: PKR {hussain.monthly_deduction:,.2f}")
        print(f"   URL: http://localhost:8002/reports/staff-statement-pdf-enhanced/{hussain.id}")
    else:
        print("❌ Muhammad Hussain not found")
    
    print("\n" + "="*60)
    print("FINANCIAL SUMMARY URL:")
    print("="*60)
    print("http://localhost:8002/reports/financial-summary-pdf-enhanced")
    print("="*60 + "\n")
    
    # Show all vendors and staff for reference
    print("\n" + "="*60)
    print("ALL VENDORS IN DATABASE:")
    print("="*60)
    vendors = db.query(Vendor).all()
    for v in vendors:
        print(f"ID: {v.id:3d} | {v.name:30s} | Balance: PKR {v.current_balance:,.2f}")
    
    print("\n" + "="*60)
    print("ALL STAFF IN DATABASE:")
    print("="*60)
    staff = db.query(Staff).all()
    for s in staff:
        print(f"ID: {s.id:3d} | {s.name:25s} | Advance: PKR {s.advance_balance:,.2f}")
    
    print("\n")
    
    db.close()

if __name__ == "__main__":
    find_sample_ids()

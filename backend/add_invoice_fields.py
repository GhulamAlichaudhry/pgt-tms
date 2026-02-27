"""
Database Migration: Add Invoice PDF Storage Fields
Run this script to add new fields to Receivable model
"""
from sqlalchemy import create_engine, Column, String, DateTime, Float, Boolean, Integer, ForeignKey, text
from sqlalchemy.orm import sessionmaker
from database import engine
from models import Base
import models

def add_invoice_fields():
    """Add new fields to receivables table for invoice management"""
    
    print("🔄 Adding invoice management fields to receivables table...")
    
    try:
        # Create connection
        connection = engine.connect()
        
        # Add new columns (SQLite doesn't support IF NOT EXISTS)
        columns_to_add = [
            ("invoice_pdf_path", "ALTER TABLE receivables ADD COLUMN invoice_pdf_path VARCHAR"),
            ("invoice_generated_at", "ALTER TABLE receivables ADD COLUMN invoice_generated_at TIMESTAMP"),
            ("invoice_sent_at", "ALTER TABLE receivables ADD COLUMN invoice_sent_at TIMESTAMP"),
            ("invoice_template", "ALTER TABLE receivables ADD COLUMN invoice_template VARCHAR DEFAULT 'standard'"),
            ("custom_notes", "ALTER TABLE receivables ADD COLUMN custom_notes TEXT"),
            ("discount_amount", "ALTER TABLE receivables ADD COLUMN discount_amount FLOAT DEFAULT 0.0"),
            ("discount_percentage", "ALTER TABLE receivables ADD COLUMN discount_percentage FLOAT DEFAULT 0.0"),
            ("tax_amount", "ALTER TABLE receivables ADD COLUMN tax_amount FLOAT DEFAULT 0.0"),
            ("tax_percentage", "ALTER TABLE receivables ADD COLUMN tax_percentage FLOAT DEFAULT 0.0"),
            ("requires_approval", "ALTER TABLE receivables ADD COLUMN requires_approval BOOLEAN DEFAULT 0"),
            ("approved_by", "ALTER TABLE receivables ADD COLUMN approved_by INTEGER"),
            ("approved_at", "ALTER TABLE receivables ADD COLUMN approved_at TIMESTAMP"),
            ("approval_status", "ALTER TABLE receivables ADD COLUMN approval_status VARCHAR DEFAULT 'approved'")
        ]
        
        for column_name, sql in columns_to_add:
            try:
                connection.execute(text(sql))
                connection.commit()
                print(f"✅ Added column: {column_name}")
            except Exception as e:
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"⏭️  Column '{column_name}' already exists, skipping...")
                else:
                    print(f"⚠️  Warning for '{column_name}': {e}")
        
        connection.close()
        
        print("\n✅ Invoice management fields added successfully!")
        print("\nNew fields added:")
        print("  - invoice_pdf_path: Path to stored PDF")
        print("  - invoice_generated_at: When PDF was generated")
        print("  - invoice_sent_at: When invoice was emailed")
        print("  - invoice_template: Template type used")
        print("  - custom_notes: Custom notes for invoice")
        print("  - discount_amount: Discount in currency")
        print("  - discount_percentage: Discount percentage")
        print("  - tax_amount: Tax in currency")
        print("  - tax_percentage: Tax percentage")
        print("  - requires_approval: Approval workflow flag")
        print("  - approved_by: User who approved")
        print("  - approved_at: Approval timestamp")
        print("  - approval_status: Approval status")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error adding fields: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION: Add Invoice Management Fields")
    print("=" * 60)
    print()
    
    success = add_invoice_fields()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ MIGRATION FAILED")
        print("=" * 60)

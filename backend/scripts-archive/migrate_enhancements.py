"""
Database Migration Script for Professional Enhancements
Adds new tables: audit_logs, notifications, user_sessions, system_settings, company_settings
"""

from database import engine, SessionLocal
import models
from datetime import datetime

def migrate_database():
    """Create all new tables"""
    print("🚀 Starting database migration...")
    print("=" * 60)
    
    try:
        # Create all tables (will only create new ones)
        print("\n📊 Creating new tables...")
        models.Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        
        # Initialize company settings with defaults
        print("\n🏢 Initializing company settings...")
        db = SessionLocal()
        
        try:
            # Check if company settings already exist
            existing = db.query(models.CompanySetting).first()
            
            if not existing:
                company_settings = models.CompanySetting(
                    company_name="PGT International (Private) Limited",
                    company_address="[Your Company Address]",
                    company_phone="[Your Phone Number]",
                    company_email="[Your Email]",
                    company_website="www.pgtinternational.com",
                    tax_id="[Your Tax ID]",
                    registration_number="[Your Registration Number]",
                    fiscal_year_start_month=1,
                    default_currency="PKR",
                    date_format="YYYY-MM-DD",
                    time_zone="Asia/Karachi"
                )
                db.add(company_settings)
                db.commit()
                print("✅ Company settings initialized!")
            else:
                print("ℹ️  Company settings already exist")
            
            # Initialize some default system settings
            print("\n⚙️  Initializing system settings...")
            
            default_settings = [
                {
                    "setting_key": "session_timeout_minutes",
                    "setting_value": "30",
                    "setting_type": "number",
                    "description": "Session timeout in minutes",
                    "is_public": False
                },
                {
                    "setting_key": "password_min_length",
                    "setting_value": "8",
                    "setting_type": "number",
                    "description": "Minimum password length",
                    "is_public": False
                },
                {
                    "setting_key": "enable_email_notifications",
                    "setting_value": "false",
                    "setting_type": "boolean",
                    "description": "Enable email notifications",
                    "is_public": False
                },
                {
                    "setting_key": "notification_retention_days",
                    "setting_value": "90",
                    "setting_type": "number",
                    "description": "Days to keep read notifications",
                    "is_public": False
                },
                {
                    "setting_key": "audit_log_retention_days",
                    "setting_value": "365",
                    "setting_type": "number",
                    "description": "Days to keep audit logs",
                    "is_public": False
                },
                {
                    "setting_key": "low_cash_threshold",
                    "setting_value": "100000",
                    "setting_type": "number",
                    "description": "Low cash balance alert threshold (PKR)",
                    "is_public": False
                },
                {
                    "setting_key": "invoice_due_warning_days",
                    "setting_value": "3",
                    "setting_type": "number",
                    "description": "Days before due date to send warning",
                    "is_public": False
                }
            ]
            
            for setting_data in default_settings:
                # Check if setting already exists
                existing_setting = db.query(models.SystemSetting).filter(
                    models.SystemSetting.setting_key == setting_data["setting_key"]
                ).first()
                
                if not existing_setting:
                    setting = models.SystemSetting(**setting_data)
                    db.add(setting)
            
            db.commit()
            print("✅ System settings initialized!")
            
            # Create initial audit log entry
            print("\n📝 Creating initial audit log entry...")
            
            # Get admin user
            admin = db.query(models.User).filter(
                models.User.role == models.UserRole.ADMIN
            ).first()
            
            if admin:
                audit_log = models.AuditLog(
                    user_id=admin.id,
                    action="system_migration",
                    table_name="system",
                    description="Professional enhancements migration completed",
                    ip_address="127.0.0.1"
                )
                db.add(audit_log)
                db.commit()
                print("✅ Initial audit log created!")
            else:
                print("⚠️  No admin user found - skipping initial audit log")
            
        finally:
            db.close()
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("\n📋 New tables added:")
        print("   - audit_logs (Audit trail system)")
        print("   - notifications (In-app notifications)")
        print("   - user_sessions (Session management)")
        print("   - system_settings (System configuration)")
        print("   - company_settings (Company information)")
        
        print("\n🎉 Your system is now enhanced with professional features!")
        print("\n📖 Next steps:")
        print("   1. Review ENHANCEMENTS-IMPLEMENTED.md")
        print("   2. Update company settings in database")
        print("   3. Integrate audit logging into CRUD operations")
        print("   4. Add notification endpoints to API")
        print("   5. Update frontend to show notifications")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  PGT TMS - Professional Enhancements Migration")
    print("=" * 60)
    
    success = migrate_database()
    
    if success:
        print("\n✅ All done! Your system is ready for the next level!")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
    
    print("=" * 60 + "\n")

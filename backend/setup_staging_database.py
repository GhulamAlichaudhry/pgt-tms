"""
Setup Staging Database for PGT International TMS
Creates pgt_test_db database and initializes with sample data
"""

import mysql.connector
from mysql.connector import Error
import sys

def create_staging_database():
    """Create staging database with proper configuration"""
    
    print("=" * 60)
    print("PGT INTERNATIONAL TMS - STAGING DATABASE SETUP")
    print("=" * 60)
    print()
    
    # Get database credentials
    print("Please provide your cPanel MySQL credentials:")
    print()
    
    host = input("MySQL Host (default: localhost): ").strip() or "localhost"
    user = input("MySQL Username (e.g., pgtinter_user): ").strip()
    password = input("MySQL Password: ").strip()
    
    if not user or not password:
        print("❌ Error: Username and password are required!")
        sys.exit(1)
    
    # Database name (cPanel will add prefix)
    db_name = "pgt_test_db"
    full_db_name = f"{user.split('_')[0]}_{db_name}"
    
    print()
    print(f"Creating database: {full_db_name}")
    print()
    
    try:
        # Connect to MySQL
        print("Connecting to MySQL...")
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            print(f"Creating database '{full_db_name}'...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {full_db_name}")
            print(f"✅ Database '{full_db_name}' created successfully")
            
            # Grant privileges
            print(f"Granting privileges to user '{user}'...")
            cursor.execute(f"GRANT ALL PRIVILEGES ON {full_db_name}.* TO '{user}'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print(f"✅ Privileges granted to '{user}'")
            
            # Show database info
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            print()
            print("Available databases:")
            for db in databases:
                if db_name in db[0]:
                    print(f"  ✅ {db[0]}")
            
            cursor.close()
            connection.close()
            
            print()
            print("=" * 60)
            print("DATABASE SETUP COMPLETE!")
            print("=" * 60)
            print()
            print("Next steps:")
            print("1. Update backend/.env.staging with these credentials:")
            print(f"   DATABASE_URL=mysql://{user}:{password}@{host}/{full_db_name}")
            print()
            print("2. Initialize database tables:")
            print("   python3 init_database.py")
            print()
            print("3. Create admin user:")
            print("   python3 ensure_admin.py")
            print()
            
            return True
            
    except Error as e:
        print(f"❌ Error: {e}")
        print()
        print("Common issues:")
        print("- Incorrect username or password")
        print("- User doesn't have CREATE DATABASE privilege")
        print("- MySQL server not running")
        print()
        return False

if __name__ == "__main__":
    success = create_staging_database()
    sys.exit(0 if success else 1)

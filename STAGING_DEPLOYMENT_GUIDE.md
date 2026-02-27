# 🚀 STAGING DEPLOYMENT GUIDE

## 📋 DEPLOYMENT OVERVIEW

**Test URL:** http://64.20.56.218/~pgtinter/  
**Database:** pgt_test_db (separate from production)  
**Purpose:** Director's live audit (Hussain Stress Test & Pak Afghan Aging)  
**Status:** Ready for deployment  

---

## ⚠️ IMPORTANT NOTES

**I cannot directly deploy to your server** as it requires:
- FTP/SSH credentials
- Server access
- Database credentials
- File upload permissions

**However, I've prepared:**
- ✅ Complete deployment instructions
- ✅ Configuration files
- ✅ Database setup scripts
- ✅ Step-by-step guide
- ✅ Testing checklist

---

## 📦 DEPLOYMENT METHODS

### Method 1: cPanel File Manager (Recommended)
- Easy to use
- No technical knowledge required
- Visual interface

### Method 2: FTP (FileZilla)
- Faster for large files
- Batch upload
- Resume capability

### Method 3: SSH/Terminal
- Most efficient
- Command-line based
- Requires SSH access

---

## 🔧 PRE-DEPLOYMENT CHECKLIST

### Local Preparation:

- [ ] Backend running locally (http://localhost:8002)
- [ ] Frontend running locally (http://localhost:3000)
- [ ] Sample PDFs generated successfully
- [ ] All tests passing
- [ ] Database migrations complete

### Server Requirements:

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] MySQL/PostgreSQL database access
- [ ] Write permissions to ~/pgtinter/ folder
- [ ] .htaccess support enabled

---

## 📁 FILES TO DEPLOY

### Backend Files:
```
backend/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── crud.py
├── modern_invoice_generator.py
├── staff_ledger_generator.py
├── invoice_service.py
├── enhanced_invoice_generator.py
├── email_service.py
├── backup_service.py
├── password_reset_service.py
├── payment_reminder_service.py
├── payslip_generator.py
├── two_factor_auth.py
├── bulk_import_export.py
├── requirements.txt
├── .env.production
├── passenger_wsgi.py
└── static/
    └── logo.png (if available)
```

### Frontend Files:
```
frontend/build/
├── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── media/
├── manifest.json
└── favicon.ico
```

### Configuration Files:
```
deployment/
├── .htaccess-api
├── .htaccess-frontend
└── start-backend.sh
```

---

## 🔨 STEP-BY-STEP DEPLOYMENT

### STEP 1: Build Frontend

```bash
cd frontend
npm run build
```

This creates `frontend/build/` folder with production files.

### STEP 2: Prepare Backend Configuration

Create `backend/.env.production`:

```env
# Database Configuration
DATABASE_URL=mysql://pgtinter_user:PASSWORD@localhost/pgtinter_pgt_test_db

# API Configuration
API_URL=http://64.20.56.218/~pgtinter/api
FRONTEND_URL=http://64.20.56.218/~pgtinter

# Security
SECRET_KEY=your-secret-key-here-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (optional for testing)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Environment
ENVIRONMENT=staging
DEBUG=False
```

### STEP 3: Create Database Setup Script

Create `backend/setup_test_database.py`:

```python
"""
Setup test database for staging
"""
import mysql.connector
from mysql.connector import Error

def create_test_database():
    """Create pgt_test_db database"""
    try:
        # Connect to MySQL
        connection = mysql.connector.connect(
            host='localhost',
            user='pgtinter_user',  # Your cPanel MySQL user
            password='YOUR_PASSWORD'  # Your MySQL password
        )
        
        if connection.is_connected():
            cursor = connection.cursor()
            
            # Create database
            cursor.execute("CREATE DATABASE IF NOT EXISTS pgtinter_pgt_test_db")
            print("✅ Database 'pgtinter_pgt_test_db' created successfully")
            
            # Grant privileges
            cursor.execute("GRANT ALL PRIVILEGES ON pgtinter_pgt_test_db.* TO 'pgtinter_user'@'localhost'")
            cursor.execute("FLUSH PRIVILEGES")
            print("✅ Privileges granted")
            
            cursor.close()
            connection.close()
            
    except Error as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_test_database()
```

### STEP 4: Upload Files via cPanel

**A. Upload Backend:**

1. Login to cPanel
2. Open File Manager
3. Navigate to `public_html/pgtinter/`
4. Create folder: `api`
5. Upload all backend files to `api/` folder
6. Set permissions: 755 for folders, 644 for files

**B. Upload Frontend:**

1. In File Manager, navigate to `public_html/pgtinter/`
2. Upload all files from `frontend/build/` to `pgtinter/` folder
3. Set permissions: 755 for folders, 644 for files

**C. Upload Configuration:**

1. Copy `deployment/.htaccess-api` to `public_html/pgtinter/api/.htaccess`
2. Copy `deployment/.htaccess-frontend` to `public_html/pgtinter/.htaccess`

### STEP 5: Setup Database

**Via cPanel:**

1. Go to MySQL Databases
2. Create database: `pgtinter_pgt_test_db`
3. Create user: `pgtinter_user` (if not exists)
4. Add user to database with ALL PRIVILEGES

**Via SSH (if available):**

```bash
cd ~/public_html/pgtinter/api
python3 setup_test_database.py
python3 init_database.py
python3 ensure_admin.py
```

### STEP 6: Install Python Dependencies

**Via SSH:**

```bash
cd ~/public_html/pgtinter/api
pip3 install -r requirements.txt --user
```

**Via cPanel Terminal:**

```bash
cd public_html/pgtinter/api
python3 -m pip install -r requirements.txt --user
```

### STEP 7: Configure Passenger WSGI

Create `backend/passenger_wsgi.py`:

```python
import sys
import os

# Add your application directory to the Python path
INTERP = os.path.expanduser("~/virtualenv/pgtinter/bin/python3")
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

# Import FastAPI app
from main import app as application
```

### STEP 8: Start Backend

**Via SSH:**

```bash
cd ~/public_html/pgtinter/api
./start-backend.sh
```

**Via cPanel:**

1. Setup Python App in cPanel
2. Point to `passenger_wsgi.py`
3. Set Python version: 3.8+
4. Start application

---

## 🔧 CONFIGURATION FILES

### .htaccess for API (api/.htaccess)

```apache
# Enable CORS
Header set Access-Control-Allow-Origin "*"
Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
Header set Access-Control-Allow-Headers "Content-Type, Authorization"

# Passenger Configuration
PassengerEnabled on
PassengerAppRoot /home/pgtinter/public_html/pgtinter/api
PassengerAppType wsgi
PassengerStartupFile passenger_wsgi.py
PassengerPython /usr/bin/python3

# Rewrite rules
RewriteEngine On
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ passenger_wsgi.py/$1 [QSA,L]
```

### .htaccess for Frontend (pgtinter/.htaccess)

```apache
# React Router Support
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /~pgtinter/
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME} !-l
  RewriteRule . /~pgtinter/index.html [L]
</IfModule>

# Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript
</IfModule>

# Caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/gif "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
</IfModule>
```

### Frontend Environment (.env.production)

Update `frontend/.env.production`:

```env
REACT_APP_API_URL=http://64.20.56.218/~pgtinter/api
REACT_APP_ENVIRONMENT=staging
```

Then rebuild:

```bash
cd frontend
npm run build
```

---

## 🧪 TESTING CHECKLIST

### After Deployment:

**1. Backend API Test:**

```bash
# Test API is running
curl http://64.20.56.218/~pgtinter/api/

# Test login
curl -X POST http://64.20.56.218/~pgtinter/api/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**2. Frontend Test:**

- [ ] Open: http://64.20.56.218/~pgtinter/
- [ ] Login page loads
- [ ] Can login with admin/admin123
- [ ] Dashboard displays
- [ ] All pages accessible

**3. Invoice Test:**

- [ ] Navigate to Receivables
- [ ] Click invoice button
- [ ] PDF generates successfully
- [ ] Red/Black theme visible
- [ ] All fields populated

**4. Hussain Statement Test:**

- [ ] Navigate to Staff Payroll
- [ ] Generate Hussain statement
- [ ] Running balance visible
- [ ] 140,000/- shown correctly
- [ ] Recovery schedule accurate

---

## 🎯 DIRECTOR'S AUDIT TESTS

### Test 1: Hussain Stress Test

**Objective:** Verify running balance calculations

**Steps:**
1. Login to staging: http://64.20.56.218/~pgtinter/
2. Go to Staff Payroll
3. Find Muhammad Hussain
4. Generate recovery statement
5. Verify:
   - [ ] Current balance: PKR 140,000/-
   - [ ] Running balance column visible (far right)
   - [ ] Color-coded red for outstanding
   - [ ] Recovery schedule: 28 months
   - [ ] All transactions listed
   - [ ] Calculations accurate

### Test 2: Pak Afghan Aging Audit

**Objective:** Verify client ledger with 30-day highlighting

**Steps:**
1. Go to Financial Ledgers
2. Select Pak Afghan client
3. Generate ledger report
4. Verify:
   - [ ] Transactions grouped by month
   - [ ] January subtotal shown
   - [ ] February subtotal shown
   - [ ] Balances older than 30 days highlighted in RED
   - [ ] Running balance accurate
   - [ ] All dates correct

### Test 3: Invoice Generation

**Objective:** Verify 412,000/- rate protection

**Steps:**
1. Go to Receivables
2. Find Fauji Foods invoice
3. Generate invoice PDF
4. Verify:
   - [ ] Amount: PKR 412,000/-
   - [ ] Halting: PKR 500/-
   - [ ] Total: PKR 412,500/-
   - [ ] Non-editable warning visible
   - [ ] QR code present
   - [ ] Red/Black theme applied
   - [ ] All fields correct

---

## 🚨 TROUBLESHOOTING

### Issue: Backend not starting

**Solution:**
```bash
# Check Python version
python3 --version

# Check dependencies
pip3 list

# Check logs
tail -f ~/logs/pgtinter_error.log
```

### Issue: Database connection failed

**Solution:**
1. Verify database exists in cPanel
2. Check username/password in .env.production
3. Ensure user has privileges
4. Test connection:
```python
import mysql.connector
conn = mysql.connector.connect(
    host='localhost',
    user='pgtinter_user',
    password='YOUR_PASSWORD',
    database='pgtinter_pgt_test_db'
)
print("Connected!" if conn.is_connected() else "Failed")
```

### Issue: Frontend shows blank page

**Solution:**
1. Check browser console for errors
2. Verify API_URL in .env.production
3. Rebuild frontend:
```bash
cd frontend
npm run build
```
4. Re-upload build files

### Issue: CORS errors

**Solution:**
Add to `backend/main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://64.20.56.218"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📞 DEPLOYMENT SUPPORT

### What I Can Help With:

- ✅ Configuration file creation
- ✅ Code modifications
- ✅ Database scripts
- ✅ Troubleshooting errors
- ✅ Testing procedures

### What Requires Manual Action:

- ❌ Actual file upload (need FTP/cPanel access)
- ❌ Database creation (need MySQL credentials)
- ❌ Server configuration (need SSH access)
- ❌ DNS/domain setup (need hosting panel access)

---

## 🎯 QUICK DEPLOYMENT SUMMARY

### For cPanel Users:

1. **Build Frontend:** `npm run build`
2. **Upload Files:**
   - Backend → `public_html/pgtinter/api/`
   - Frontend → `public_html/pgtinter/`
3. **Create Database:** `pgtinter_pgt_test_db`
4. **Update .env.production** with database credentials
5. **Install Dependencies:** `pip3 install -r requirements.txt`
6. **Initialize Database:** `python3 init_database.py`
7. **Start Backend:** Setup Python App in cPanel
8. **Test:** http://64.20.56.218/~pgtinter/

### For SSH Users:

```bash
# 1. Upload files via SCP/SFTP
scp -r backend/* user@64.20.56.218:~/public_html/pgtinter/api/
scp -r frontend/build/* user@64.20.56.218:~/public_html/pgtinter/

# 2. SSH into server
ssh user@64.20.56.218

# 3. Setup database
cd ~/public_html/pgtinter/api
python3 setup_test_database.py
python3 init_database.py

# 4. Install dependencies
pip3 install -r requirements.txt --user

# 5. Start backend
./start-backend.sh

# 6. Test
curl http://64.20.56.218/~pgtinter/api/
```

---

## ✅ DEPLOYMENT CHECKLIST

### Pre-Deployment:
- [ ] Frontend built (`npm run build`)
- [ ] .env.production configured
- [ ] Database credentials ready
- [ ] Server access confirmed

### Deployment:
- [ ] Backend files uploaded
- [ ] Frontend files uploaded
- [ ] .htaccess files in place
- [ ] Database created
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Backend started

### Post-Deployment:
- [ ] API responds
- [ ] Frontend loads
- [ ] Login works
- [ ] Dashboard displays
- [ ] Invoices generate
- [ ] Statements generate
- [ ] All tests pass

### Director's Audit:
- [ ] Hussain Stress Test complete
- [ ] Pak Afghan Aging verified
- [ ] Invoice generation tested
- [ ] All calculations accurate
- [ ] Ready for production

---

## 🎉 READY FOR STAGING

**Status:** Deployment guide complete  
**Next Step:** Manual deployment to server  
**Test URL:** http://64.20.56.218/~pgtinter/  
**Database:** pgtinter_pgt_test_db  

**Once deployed, Director can perform:**
- ✅ Hussain Stress Test (140,000/- running balance)
- ✅ Pak Afghan Aging Audit (30-day highlighting)
- ✅ Invoice Generation Test (412,500/- rate protection)
- ✅ Complete system validation

---

**I've prepared everything needed for deployment. You'll need to manually upload files and configure the server using the instructions above.** 🚀


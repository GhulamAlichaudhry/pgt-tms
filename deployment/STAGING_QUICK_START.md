# ⚡ STAGING DEPLOYMENT - QUICK START

## 🎯 DEPLOYMENT TARGET

**URL:** http://64.20.56.218/~pgtinter/  
**Database:** pgtinter_pgt_test_db  
**Purpose:** Director's Live Audit  
**Time Required:** 20-30 minutes  

---

## 📋 PRE-DEPLOYMENT CHECKLIST

Before you start, ensure you have:

- [ ] cPanel login credentials
- [ ] MySQL database access
- [ ] FTP/File Manager access
- [ ] SSH access (optional, but helpful)
- [ ] Local system ready (backend & frontend running)

---

## 🚀 DEPLOYMENT STEPS

### STEP 1: Build Frontend (5 minutes)

On your local machine:

```bash
# Navigate to frontend folder
cd frontend

# Copy staging environment file
copy .env.staging .env

# Install dependencies (if not already done)
npm install

# Build for production
npm run build
```

**Expected Output:** `frontend/build/` folder created with all static files

---

### STEP 2: Prepare Backend Files (2 minutes)

On your local machine:

```bash
# Navigate to backend folder
cd backend

# Copy staging environment file
copy .env.staging .env.production

# Note: You'll update database credentials after creating the database
```

---

### STEP 3: Login to cPanel

1. Open browser: Your cPanel URL
2. Username: pgtinter
3. Password: Your password
4. Navigate to File Manager

---

### STEP 4: Create Directory Structure (2 minutes)

In cPanel File Manager:

1. Navigate to `public_html/`
2. Create new folder: `pgtinter`
3. Inside `pgtinter/`, create folder: `api`

**Structure:**
```
public_html/
└── pgtinter/
    └── api/
```

---

### STEP 5: Upload Backend Files (5 minutes)

Upload these files to `public_html/pgtinter/api/`:

**Core Files:**
- main.py
- database.py
- models.py
- schemas.py
- auth.py
- crud.py
- validators.py

**Service Files:**
- modern_invoice_generator.py
- staff_ledger_generator.py
- invoice_service.py
- enhanced_invoice_generator.py
- email_service.py
- backup_service.py
- password_reset_service.py
- payment_reminder_service.py
- payslip_generator.py
- two_factor_auth.py
- bulk_import_export.py
- notification_service.py
- ledger_service.py
- ledger_engine.py
- financial_calculator.py
- cash_register_service.py
- audit_service.py
- report_generator.py
- company_config.py

**Setup Files:**
- requirements.txt
- passenger_wsgi.py
- init_database.py
- ensure_admin.py
- setup_staging_database.py
- .env.staging (rename to .env.production after upload)

**Configuration:**
- Upload `deployment/.htaccess-staging-api` as `api/.htaccess`

---

### STEP 6: Upload Frontend Files (5 minutes)

Upload ALL files from `frontend/build/` to `public_html/pgtinter/`:

**Files to upload:**
- index.html
- manifest.json
- favicon.ico
- robots.txt
- asset-manifest.json
- static/ folder (complete with all subfolders)

**Configuration:**
- Upload `deployment/.htaccess-staging-frontend` as `.htaccess`

---

### STEP 7: Create Database (3 minutes)

**Option A: Via cPanel MySQL Databases**

1. Go to cPanel → MySQL Databases
2. Create New Database:
   - Name: `pgt_test_db`
   - Full name will be: `pgtinter_pgt_test_db`
3. Create User (if not exists):
   - Username: `pgtinter_user`
   - Password: [Strong password]
4. Add User to Database:
   - User: `pgtinter_user`
   - Database: `pgtinter_pgt_test_db`
   - Privileges: ALL PRIVILEGES

**Option B: Via SSH**

```bash
cd ~/public_html/pgtinter/api
python3 setup_staging_database.py
```

---

### STEP 8: Configure Database Connection (2 minutes)

1. In File Manager, navigate to `public_html/pgtinter/api/`
2. Edit `.env.production`
3. Update database credentials:

```env
DATABASE_URL=mysql://pgtinter_user:YOUR_PASSWORD@localhost/pgtinter_pgt_test_db
```

**Replace:**
- `YOUR_PASSWORD` with your actual MySQL password

---

### STEP 9: Install Python Dependencies (3 minutes)

**Via cPanel Terminal:**

```bash
cd ~/public_html/pgtinter/api
python3 -m pip install -r requirements.txt --user
```

**Via SSH:**

```bash
cd ~/public_html/pgtinter/api
pip3 install -r requirements.txt --user
```

**Expected packages:**
- fastapi
- uvicorn
- sqlalchemy
- python-jose
- passlib
- python-multipart
- reportlab
- qrcode[pil]
- mysql-connector-python
- python-dotenv
- And more...

---

### STEP 10: Initialize Database (2 minutes)

**Via cPanel Terminal or SSH:**

```bash
cd ~/public_html/pgtinter/api

# Initialize database tables
python3 init_database.py

# Create admin user
python3 ensure_admin.py
```

**Expected Output:**
```
✅ Database initialized successfully
✅ Admin user created: admin / admin123
```

---

### STEP 11: Start Backend (2 minutes)

**Option A: Via cPanel Python App**

1. Go to cPanel → Setup Python App
2. Click "Create Application"
3. Settings:
   - Python version: 3.8 or higher
   - Application root: `/home/pgtinter/public_html/pgtinter/api`
   - Application URL: `pgtinter/api`
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`
4. Click "Create"
5. Start the application

**Option B: Via SSH**

```bash
cd ~/public_html/pgtinter/api
chmod +x start-backend.sh
./start-backend.sh
```

---

### STEP 12: Test Deployment (3 minutes)

**Test Backend API:**

Open browser:
```
http://64.20.56.218/~pgtinter/api/
```

**Expected Response:**
```json
{"message": "PGT TMS API", "version": "1.0", "status": "running"}
```

**Test Frontend:**

Open browser:
```
http://64.20.56.218/~pgtinter/
```

**Expected:** Login page loads with PGT International branding

**Test Login:**

- Username: `admin`
- Password: `admin123`

**Expected:** Dashboard loads successfully

---

## 🧪 DIRECTOR'S AUDIT TESTS

Once deployed, perform these critical tests:

### Test 1: Hussain Stress Test ✅

**Objective:** Verify running balance calculations

**Steps:**
1. Login to http://64.20.56.218/~pgtinter/
2. Navigate to Staff Payroll
3. Find Muhammad Hussain (EMP-001)
4. Click "Generate Statement"
5. Download PDF

**Verify:**
- [ ] Current balance: PKR 140,000/-
- [ ] Running balance column visible (far right)
- [ ] Color-coded red for outstanding
- [ ] Recovery schedule: 28 months @ PKR 5,000/month
- [ ] All transactions listed chronologically
- [ ] Bank statement format
- [ ] Red/Black theme applied

---

### Test 2: Pak Afghan Aging Audit ✅

**Objective:** Verify 30-day aging highlights

**Steps:**
1. Navigate to Financial Ledgers
2. Select "Pak Afghan" client
3. Generate ledger report
4. Download PDF

**Verify:**
- [ ] Transactions grouped by month
- [ ] January subtotal shown
- [ ] February subtotal shown
- [ ] Balances older than 30 days highlighted in RED
- [ ] Running balance accurate
- [ ] All dates correct
- [ ] Professional appearance

---

### Test 3: Invoice Generation ✅

**Objective:** Verify rate protection and professional appearance

**Steps:**
1. Navigate to Receivables
2. Find Fauji Foods invoice
3. Click "Generate Invoice"
4. Download PDF

**Verify:**
- [ ] Amount: PKR 412,000/-
- [ ] Halting: PKR 500/-
- [ ] Total: PKR 412,500/-
- [ ] "COMMERCIAL INVOICE" header
- [ ] Trip Summary Box complete
- [ ] Container # field visible
- [ ] Product (not Cargo) shown
- [ ] Meezan Bank details
- [ ] Faysal Bank details
- [ ] QR code present
- [ ] Terms & Conditions visible
- [ ] Non-editable warning
- [ ] Red/Black theme applied
- [ ] Professional appearance

---

## 🚨 TROUBLESHOOTING

### Issue: Backend not responding

**Check:**
```bash
# Via SSH
cd ~/public_html/pgtinter/api
tail -f ~/logs/pgtinter_error.log
```

**Solutions:**
1. Verify Python dependencies installed
2. Check .env.production database credentials
3. Restart Python app in cPanel
4. Check file permissions (755 for folders, 644 for files)

---

### Issue: Frontend shows blank page

**Check:**
1. Browser console (F12) for errors
2. Verify .env.staging was used during build
3. Check .htaccess file is present

**Solutions:**
1. Rebuild frontend with correct .env.staging
2. Clear browser cache
3. Verify API_URL in build: `http://64.20.56.218/~pgtinter/api`

---

### Issue: Database connection error

**Check:**
```bash
# Test database connection
cd ~/public_html/pgtinter/api
python3 -c "import mysql.connector; conn = mysql.connector.connect(host='localhost', user='pgtinter_user', password='YOUR_PASSWORD', database='pgtinter_pgt_test_db'); print('Connected!' if conn.is_connected() else 'Failed')"
```

**Solutions:**
1. Verify database name: `pgtinter_pgt_test_db`
2. Check user has ALL PRIVILEGES
3. Verify password in .env.production
4. Test in cPanel → phpMyAdmin

---

### Issue: CORS errors

**Check:**
1. Browser console shows CORS error
2. API requests blocked

**Solutions:**
1. Verify .htaccess files are in place
2. Check CORS headers in backend/main.py
3. Add to main.py if missing:

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

### Issue: Invoice/Statement not generating

**Check:**
1. Python dependencies installed (reportlab, qrcode)
2. File permissions for invoices/ folder
3. Backend logs for errors

**Solutions:**
```bash
# Install missing dependencies
cd ~/public_html/pgtinter/api
pip3 install reportlab qrcode[pil] --user

# Create invoices folder
mkdir -p invoices
chmod 755 invoices
```

---

## ✅ DEPLOYMENT COMPLETE CHECKLIST

### Backend:
- [ ] All Python files uploaded
- [ ] .htaccess in place
- [ ] .env.production configured
- [ ] Dependencies installed
- [ ] Database created
- [ ] Database initialized
- [ ] Admin user created
- [ ] Backend started
- [ ] API responds at /api/

### Frontend:
- [ ] Build files uploaded
- [ ] .htaccess in place
- [ ] Static files accessible
- [ ] Login page loads
- [ ] Can login successfully
- [ ] Dashboard displays
- [ ] All pages accessible

### Testing:
- [ ] Hussain statement generates
- [ ] Pak Afghan ledger generates
- [ ] Invoice generates
- [ ] All PDFs download
- [ ] Red/Black theme visible
- [ ] Calculations accurate
- [ ] No console errors

### Director's Audit:
- [ ] Hussain Stress Test passed
- [ ] Pak Afghan Aging verified
- [ ] Invoice generation confirmed
- [ ] Rate protection verified (412,500/-)
- [ ] Running balance accurate (140,000/-)
- [ ] Professional appearance confirmed

---

## 🎉 SUCCESS!

**Your staging system is now live at:**
http://64.20.56.218/~pgtinter/

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

**Ready for Director's audit:**
- ✅ Hussain Stress Test
- ✅ Pak Afghan Aging Audit
- ✅ Invoice Generation Test

---

## 📞 NEED HELP?

If you encounter any issues:

1. Check the troubleshooting section above
2. Review error logs in cPanel
3. Verify all files uploaded correctly
4. Test database connection
5. Check file permissions

**Common commands:**
```bash
# Check Python version
python3 --version

# List installed packages
pip3 list

# Test database
python3 init_database.py

# View logs
tail -f ~/logs/pgtinter_error.log
```

---

**Deployment time: 20-30 minutes**  
**Status: Ready for live audit** ✅

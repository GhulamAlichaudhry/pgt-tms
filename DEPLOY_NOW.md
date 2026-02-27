# 🚀 DEPLOY NOW - STAGING DEPLOYMENT

## ⚡ FASTEST PATH TO LIVE SYSTEM

**Target:** http://64.20.56.218/~pgtinter/  
**Time:** 20-30 minutes  
**Method:** cPanel File Manager  

---

## 🎯 WHAT YOU'RE DEPLOYING

✅ Modern Commercial Invoice System (Red/Black Theme)  
✅ Staff Ledger Generator (Bank Statement Style)  
✅ Complete Transport Management System  
✅ 16 Functional Modules  
✅ Sample Data for Testing  

---

## 📋 BEFORE YOU START

**You Need:**
- [ ] cPanel login (username: pgtinter)
- [ ] MySQL database access
- [ ] 20-30 minutes of time
- [ ] This guide open

**On Your Computer:**
- [ ] Backend folder ready
- [ ] Frontend folder ready
- [ ] Node.js installed (for building frontend)

---

## 🚀 STEP-BY-STEP DEPLOYMENT

### STEP 1: Build Frontend (5 min)

Open PowerShell/Terminal on your computer:

```powershell
# Navigate to frontend
cd frontend

# Copy staging environment
copy .env.staging .env

# Build for production
npm run build
```

**Wait for:** "Compiled successfully!" message  
**Result:** `frontend/build/` folder created  

---

### STEP 2: Login to cPanel (1 min)

1. Open browser
2. Go to your cPanel URL
3. Username: `pgtinter`
4. Password: [Your password]
5. Click "File Manager"

---

### STEP 3: Create Folders (1 min)

In File Manager:

1. Navigate to `public_html/`
2. Click "New Folder" → Name: `pgtinter`
3. Open `pgtinter/` folder
4. Click "New Folder" → Name: `api`

**Result:**
```
public_html/
└── pgtinter/
    └── api/
```

---

### STEP 4: Upload Backend (5 min)

**Navigate to:** `public_html/pgtinter/api/`

**Click "Upload"** and select these files from your `backend/` folder:

**Core Files (Must Upload):**
- main.py
- database.py
- models.py
- schemas.py
- auth.py
- crud.py
- validators.py

**Generators (Must Upload):**
- modern_invoice_generator.py
- staff_ledger_generator.py
- invoice_service.py
- enhanced_invoice_generator.py

**Services (Must Upload):**
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

**Setup Files (Must Upload):**
- requirements.txt
- passenger_wsgi.py
- init_database.py
- ensure_admin.py
- setup_staging_database.py

**Configuration:**
- Upload `.env.staging` and rename to `.env.production`
- Upload `deployment/.htaccess-staging-api` and rename to `.htaccess`

---

### STEP 5: Upload Frontend (5 min)

**Navigate to:** `public_html/pgtinter/`

**Upload ALL files from:** `frontend/build/` folder

**Files to upload:**
- index.html
- manifest.json
- favicon.ico
- robots.txt
- asset-manifest.json
- **static/** folder (complete - drag and drop entire folder)

**Configuration:**
- Upload `deployment/.htaccess-staging-frontend` and rename to `.htaccess`

---

### STEP 6: Create Database (2 min)

**In cPanel:**

1. Go back to cPanel home
2. Find "MySQL Databases"
3. Click it

**Create Database:**
- Database Name: `pgt_test_db`
- Click "Create Database"
- **Note:** Full name will be `pgtinter_pgt_test_db`

**Add User to Database:**
- User: `pgtinter_user` (create if doesn't exist)
- Database: `pgtinter_pgt_test_db`
- Privileges: Check "ALL PRIVILEGES"
- Click "Make Changes"

---

### STEP 7: Configure Database (2 min)

**In File Manager:**

1. Navigate to `public_html/pgtinter/api/`
2. Find `.env.production`
3. Right-click → "Edit"
4. Find line: `DATABASE_URL=...`
5. Change to:
```
DATABASE_URL=mysql://pgtinter_user:YOUR_PASSWORD@localhost/pgtinter_pgt_test_db
```
6. Replace `YOUR_PASSWORD` with your actual MySQL password
7. Click "Save Changes"

---

### STEP 8: Install Dependencies (3 min)

**In cPanel:**

1. Go back to cPanel home
2. Find "Terminal" (or "SSH Access")
3. Click it
4. Run these commands:

```bash
cd ~/public_html/pgtinter/api
python3 -m pip install -r requirements.txt --user
```

**Wait for:** All packages to install (2-3 minutes)

---

### STEP 9: Initialize Database (2 min)

**In Terminal (same window):**

```bash
# Still in ~/public_html/pgtinter/api

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

### STEP 10: Start Backend (2 min)

**Option A: Via cPanel Python App**

1. Go to cPanel home
2. Find "Setup Python App"
3. Click "Create Application"
4. Fill in:
   - Python version: 3.8 or higher
   - Application root: `/home/pgtinter/public_html/pgtinter/api`
   - Application URL: `pgtinter/api`
   - Application startup file: `passenger_wsgi.py`
   - Application Entry point: `application`
5. Click "Create"
6. Click "Start" (or "Restart")

**Option B: Via Terminal**

```bash
cd ~/public_html/pgtinter/api
chmod +x start-backend.sh
./start-backend.sh
```

---

### STEP 11: TEST! (3 min)

**Test Backend:**

Open browser:
```
http://64.20.56.218/~pgtinter/api/
```

**Expected:**
```json
{"message": "PGT TMS API", "version": "1.0", "status": "running"}
```

**Test Frontend:**

Open browser:
```
http://64.20.56.218/~pgtinter/
```

**Expected:** Login page loads

**Test Login:**
- Username: `admin`
- Password: `admin123`
- Click "Login"

**Expected:** Dashboard loads with all modules

---

## 🎯 DIRECTOR'S AUDIT (10 min)

### Test 1: Hussain Stress Test

1. Click "Staff Payroll" in sidebar
2. Find "Muhammad Hussain"
3. Click "Generate Statement"
4. PDF downloads

**Verify:**
- ✅ Balance: PKR 140,000/-
- ✅ Running balance column (far right)
- ✅ Red color for outstanding
- ✅ 28 months remaining
- ✅ Bank statement format

---

### Test 2: Invoice Generation

1. Click "Receivables" in sidebar
2. Find any receivable
3. Click "Generate Invoice"
4. PDF downloads

**Verify:**
- ✅ "COMMERCIAL INVOICE" header
- ✅ Red/Black theme
- ✅ Trip Summary Box
- ✅ Container # field
- ✅ Product (not Cargo)
- ✅ Halting charges column
- ✅ Meezan Bank details
- ✅ Faysal Bank details
- ✅ QR code
- ✅ Terms & Conditions
- ✅ Non-editable warning

---

### Test 3: Pak Afghan Aging

1. Click "Financial Ledgers"
2. Select "Pak Afghan" client
3. Generate report
4. PDF downloads

**Verify:**
- ✅ Monthly grouping
- ✅ Subtotals visible
- ✅ 30-day aging in RED
- ✅ Running balance accurate

---

## ✅ DEPLOYMENT COMPLETE!

**If all tests pass:**

🎉 **CONGRATULATIONS!**

Your staging system is now LIVE at:
**http://64.20.56.218/~pgtinter/**

**Login:**
- Username: `admin`
- Password: `admin123`

**Ready for:**
- ✅ Director's live audit
- ✅ Hussain stress test
- ✅ Pak Afghan aging verification
- ✅ Invoice generation testing
- ✅ Full system evaluation

---

## 🚨 IF SOMETHING DOESN'T WORK

### Backend not responding?

```bash
# In Terminal
cd ~/public_html/pgtinter/api
tail -f ~/logs/pgtinter_error.log
```

**Common fixes:**
1. Restart Python app in cPanel
2. Check .env.production database credentials
3. Verify all files uploaded
4. Check file permissions

---

### Frontend blank page?

**Check:**
1. Browser console (Press F12)
2. Look for errors

**Fix:**
1. Verify .env.staging was used during build
2. Rebuild frontend:
```bash
cd frontend
copy .env.staging .env
npm run build
```
3. Re-upload build files

---

### Database error?

**Check:**
1. Database name: `pgtinter_pgt_test_db`
2. User: `pgtinter_user`
3. Password in .env.production

**Fix:**
1. Go to cPanel → MySQL Databases
2. Verify database exists
3. Verify user has ALL PRIVILEGES
4. Update .env.production

---

### Invoice not generating?

```bash
# In Terminal
cd ~/public_html/pgtinter/api
pip3 install reportlab qrcode[pil] --user
mkdir -p invoices
chmod 755 invoices
```

---

## 📞 QUICK REFERENCE

**URLs:**
- Frontend: http://64.20.56.218/~pgtinter/
- Backend: http://64.20.56.218/~pgtinter/api/

**Login:**
- Username: `admin`
- Password: `admin123`

**Database:**
- Name: `pgtinter_pgt_test_db`
- User: `pgtinter_user`

**Folders:**
- Backend: `~/public_html/pgtinter/api/`
- Frontend: `~/public_html/pgtinter/`

**Commands:**
```bash
# Navigate to backend
cd ~/public_html/pgtinter/api

# View logs
tail -f ~/logs/pgtinter_error.log

# Restart backend
# (Use cPanel Python App interface)

# Test database
python3 init_database.py
```

---

## 📚 DETAILED GUIDES

**For more details, see:**
- `deployment/STAGING_QUICK_START.md` - Detailed quick start
- `STAGING_DEPLOYMENT_GUIDE.md` - Complete guide
- `STAGING_DEPLOYMENT_PACKAGE.md` - Full package info

---

## 🎊 YOU'RE READY!

**Follow the steps above and you'll have a live system in 20-30 minutes!**

**Start with STEP 1 and work your way through.**

**Each step is simple and clearly explained.**

**You've got this!** 💪

---

**DEPLOY NOW!** 🚀

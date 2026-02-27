# ✅ STAGING DEPLOYMENT - VISUAL CHECKLIST

## 🎯 TARGET: http://64.20.56.218/~pgtinter/

---

## 📦 PHASE 1: PRE-DEPLOYMENT (5 minutes)

### Local Preparation:
```
[ ] Open PowerShell/Terminal
[ ] Navigate to project folder
[ ] Verify backend folder exists
[ ] Verify frontend folder exists
[ ] Read DEPLOY_NOW.md
```

### Build Frontend:
```
[ ] cd frontend
[ ] copy .env.staging .env
[ ] npm install (if needed)
[ ] npm run build
[ ] Verify build/ folder created
[ ] Check build/ has index.html
[ ] Check build/ has static/ folder
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🌐 PHASE 2: SERVER ACCESS (2 minutes)

### cPanel Login:
```
[ ] Open browser
[ ] Go to cPanel URL
[ ] Enter username: pgtinter
[ ] Enter password
[ ] Login successful
[ ] Open File Manager
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 📁 PHASE 3: CREATE FOLDERS (1 minute)

### Directory Structure:
```
[ ] Navigate to public_html/
[ ] Create folder: pgtinter
[ ] Open pgtinter/ folder
[ ] Create folder: api
[ ] Verify structure:
    public_html/
    └── pgtinter/
        └── api/
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## ⬆️ PHASE 4: UPLOAD BACKEND (5 minutes)

### Navigate:
```
[ ] Go to public_html/pgtinter/api/
[ ] Click "Upload" button
```

### Core Files:
```
[ ] main.py
[ ] database.py
[ ] models.py
[ ] schemas.py
[ ] auth.py
[ ] crud.py
[ ] validators.py
```

### Generators:
```
[ ] modern_invoice_generator.py
[ ] staff_ledger_generator.py
[ ] invoice_service.py
[ ] enhanced_invoice_generator.py
[ ] payslip_generator.py
[ ] report_generator.py
```

### Services:
```
[ ] email_service.py
[ ] backup_service.py
[ ] password_reset_service.py
[ ] payment_reminder_service.py
[ ] two_factor_auth.py
[ ] bulk_import_export.py
[ ] notification_service.py
[ ] ledger_service.py
[ ] ledger_engine.py
[ ] financial_calculator.py
[ ] cash_register_service.py
[ ] audit_service.py
[ ] company_config.py
```

### Setup Files:
```
[ ] requirements.txt
[ ] passenger_wsgi.py
[ ] init_database.py
[ ] ensure_admin.py
[ ] setup_staging_database.py
```

### Configuration:
```
[ ] Upload .env.staging
[ ] Rename to .env.production
[ ] Upload deployment/.htaccess-staging-api
[ ] Rename to .htaccess
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## ⬆️ PHASE 5: UPLOAD FRONTEND (5 minutes)

### Navigate:
```
[ ] Go to public_html/pgtinter/
[ ] Click "Upload" button
```

### Build Files:
```
[ ] index.html
[ ] manifest.json
[ ] favicon.ico
[ ] robots.txt
[ ] asset-manifest.json
[ ] static/ folder (complete)
    [ ] static/css/
    [ ] static/js/
    [ ] static/media/
```

### Configuration:
```
[ ] Upload deployment/.htaccess-staging-frontend
[ ] Rename to .htaccess
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🗄️ PHASE 6: DATABASE SETUP (3 minutes)

### Create Database:
```
[ ] Go to cPanel home
[ ] Click "MySQL Databases"
[ ] Create database: pgt_test_db
[ ] Note full name: pgtinter_pgt_test_db
```

### Create/Verify User:
```
[ ] User: pgtinter_user
[ ] Password: [Your password]
[ ] Create user (if doesn't exist)
```

### Grant Privileges:
```
[ ] Add user to database
[ ] Select: pgtinter_pgt_test_db
[ ] Check: ALL PRIVILEGES
[ ] Click "Make Changes"
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## ⚙️ PHASE 7: CONFIGURE (2 minutes)

### Update .env.production:
```
[ ] Go to public_html/pgtinter/api/
[ ] Right-click .env.production
[ ] Click "Edit"
[ ] Find: DATABASE_URL=...
[ ] Change to:
    DATABASE_URL=mysql://pgtinter_user:YOUR_PASSWORD@localhost/pgtinter_pgt_test_db
[ ] Replace YOUR_PASSWORD with actual password
[ ] Save changes
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 📦 PHASE 8: INSTALL DEPENDENCIES (3 minutes)

### Open Terminal:
```
[ ] Go to cPanel home
[ ] Click "Terminal"
[ ] Terminal opens
```

### Install Packages:
```
[ ] cd ~/public_html/pgtinter/api
[ ] python3 -m pip install -r requirements.txt --user
[ ] Wait for installation (2-3 minutes)
[ ] Verify: "Successfully installed..." messages
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🗄️ PHASE 9: INITIALIZE DATABASE (2 minutes)

### Run Setup Scripts:
```
[ ] cd ~/public_html/pgtinter/api (if not already there)
[ ] python3 init_database.py
[ ] Verify: "✅ Database initialized successfully"
[ ] python3 ensure_admin.py
[ ] Verify: "✅ Admin user created: admin / admin123"
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🚀 PHASE 10: START BACKEND (2 minutes)

### Option A: cPanel Python App:
```
[ ] Go to cPanel home
[ ] Click "Setup Python App"
[ ] Click "Create Application"
[ ] Python version: 3.8+
[ ] Application root: /home/pgtinter/public_html/pgtinter/api
[ ] Application URL: pgtinter/api
[ ] Startup file: passenger_wsgi.py
[ ] Entry point: application
[ ] Click "Create"
[ ] Click "Start"
```

### Option B: Terminal:
```
[ ] cd ~/public_html/pgtinter/api
[ ] chmod +x start-backend.sh
[ ] ./start-backend.sh
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🧪 PHASE 11: TESTING (5 minutes)

### Test Backend API:
```
[ ] Open browser
[ ] Go to: http://64.20.56.218/~pgtinter/api/
[ ] Expected: {"message": "PGT TMS API", ...}
[ ] Status: Working ✅
```

### Test Frontend:
```
[ ] Open browser
[ ] Go to: http://64.20.56.218/~pgtinter/
[ ] Expected: Login page loads
[ ] Status: Working ✅
```

### Test Login:
```
[ ] Username: admin
[ ] Password: admin123
[ ] Click "Login"
[ ] Expected: Dashboard loads
[ ] Status: Working ✅
```

### Test Navigation:
```
[ ] Click "Dashboard" - Loads ✅
[ ] Click "Fleet Logs" - Loads ✅
[ ] Click "Receivables" - Loads ✅
[ ] Click "Staff Payroll" - Loads ✅
[ ] Click "Financial Ledgers" - Loads ✅
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## 🎯 PHASE 12: DIRECTOR'S AUDIT (10 minutes)

### Test 1: Hussain Stress Test
```
[ ] Navigate to Staff Payroll
[ ] Find Muhammad Hussain
[ ] Click "Generate Statement"
[ ] PDF downloads
[ ] Open PDF
[ ] Verify: Balance PKR 140,000/- ✅
[ ] Verify: Running balance column (far right) ✅
[ ] Verify: Color-coded red ✅
[ ] Verify: 28 months remaining ✅
[ ] Verify: Bank statement format ✅
[ ] Verify: Red/Black theme ✅
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### Test 2: Invoice Generation
```
[ ] Navigate to Receivables
[ ] Find any receivable
[ ] Click "Generate Invoice"
[ ] PDF downloads
[ ] Open PDF
[ ] Verify: "COMMERCIAL INVOICE" header ✅
[ ] Verify: NTN and address ✅
[ ] Verify: Trip Summary Box ✅
[ ] Verify: Container # field ✅
[ ] Verify: Product (not Cargo) ✅
[ ] Verify: Halting charges column ✅
[ ] Verify: Meezan Bank details ✅
[ ] Verify: Faysal Bank details ✅
[ ] Verify: QR code ✅
[ ] Verify: Terms & Conditions ✅
[ ] Verify: Non-editable warning ✅
[ ] Verify: Red/Black theme ✅
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

### Test 3: Pak Afghan Aging
```
[ ] Navigate to Financial Ledgers
[ ] Select "Pak Afghan" client
[ ] Generate report
[ ] PDF downloads
[ ] Open PDF
[ ] Verify: Monthly grouping ✅
[ ] Verify: Subtotals visible ✅
[ ] Verify: 30+ days in RED ✅
[ ] Verify: Running balance accurate ✅
[ ] Verify: Professional appearance ✅
```

**Status:** ⬜ Not Started | ⏳ In Progress | ✅ Complete

---

## ✅ FINAL VERIFICATION

### System Status:
```
[ ] Frontend URL works: http://64.20.56.218/~pgtinter/
[ ] Backend API works: http://64.20.56.218/~pgtinter/api/
[ ] Login successful: admin / admin123
[ ] Dashboard displays all modules
[ ] All pages accessible
[ ] No console errors (F12)
```

### Document Generation:
```
[ ] Invoices generate successfully
[ ] Statements generate successfully
[ ] PDFs download correctly
[ ] Red/Black theme applied
[ ] All fields populated
[ ] Calculations accurate
```

### Director's Audit:
```
[ ] Hussain Stress Test: PASSED ✅
[ ] Invoice Generation: PASSED ✅
[ ] Pak Afghan Aging: PASSED ✅
```

---

## 🎉 DEPLOYMENT COMPLETE!

### Final Status:
```
✅ All phases complete
✅ All tests passed
✅ System live and operational
✅ Ready for Director's audit
```

### Access Information:
```
URL: http://64.20.56.218/~pgtinter/
Username: admin
Password: admin123
```

### Next Steps:
```
[ ] Notify Director
[ ] Schedule live audit
[ ] Prepare for production deployment
[ ] Plan domain migration
```

---

## 📊 DEPLOYMENT SUMMARY

**Total Time:** 20-30 minutes  
**Phases Completed:** 12/12  
**Tests Passed:** 3/3  
**Status:** ✅ LIVE AND OPERATIONAL  

**Deployed:**
- ✅ Modern Commercial Invoice System
- ✅ Staff Ledger Generator
- ✅ Complete TMS (16 modules)
- ✅ Sample Data
- ✅ Professional Branding

**Ready For:**
- ✅ Director's live audit
- ✅ Hussain stress test
- ✅ Pak Afghan aging verification
- ✅ Invoice generation testing
- ✅ Full system evaluation

---

## 🚨 TROUBLESHOOTING QUICK REFERENCE

### If Backend Not Working:
```bash
cd ~/public_html/pgtinter/api
pip3 install -r requirements.txt --user
python3 init_database.py
# Restart Python app in cPanel
```

### If Frontend Blank:
```bash
cd frontend
copy .env.staging .env
npm run build
# Re-upload build files
```

### If Database Error:
```
1. Check database name: pgtinter_pgt_test_db
2. Verify .env.production credentials
3. Test in phpMyAdmin
4. Check user privileges
```

### If Invoice Not Generating:
```bash
cd ~/public_html/pgtinter/api
pip3 install reportlab qrcode[pil] --user
mkdir -p invoices
chmod 755 invoices
```

---

**PRINT THIS CHECKLIST AND CHECK OFF ITEMS AS YOU COMPLETE THEM!** ✅

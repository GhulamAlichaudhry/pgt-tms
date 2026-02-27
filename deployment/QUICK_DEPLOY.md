# ⚡ QUICK DEPLOYMENT TO STAGING

## 🎯 OBJECTIVE

Deploy to: **http://64.20.56.218/~pgtinter/**  
Database: **pgtinter_pgt_test_db**  
Purpose: **Director's Live Audit**  

---

## 🚀 FASTEST DEPLOYMENT METHOD

### Option 1: cPanel File Manager (15 minutes)

**Step 1: Build Frontend (2 min)**
```bash
cd frontend
npm run build
```

**Step 2: Login to cPanel**
- URL: Your hosting cPanel URL
- Username: pgtinter
- Password: Your password

**Step 3: Upload Backend (5 min)**
1. File Manager → public_html
2. Create folder: `pgtinter/api`
3. Upload ALL files from `backend/` folder
4. Upload `deployment/.htaccess-api` as `api/.htaccess`

**Step 4: Upload Frontend (5 min)**
1. File Manager → public_html/pgtinter
2. Upload ALL files from `frontend/build/` folder
3. Upload `deployment/.htaccess-frontend` as `.htaccess`

**Step 5: Create Database (2 min)**
1. cPanel → MySQL Databases
2. Create database: `pgt_test_db`
3. Create user: `pgtinter_user` (or use existing)
4. Add user to database with ALL PRIVILEGES
5. Note: Full database name will be `pgtinter_pgt_test_db`

**Step 6: Configure Backend (1 min)**
1. File Manager → pgtinter/api
2. Edit `.env.production`
3. Update database credentials:
```env
DATABASE_URL=mysql://pgtinter_user:YOUR_PASSWORD@localhost/pgtinter_pgt_test_db
```

**Step 7: Initialize Database**
1. cPanel → Terminal
2. Run:
```bash
cd public_html/pgtinter/api
python3 init_database.py
python3 ensure_admin.py
```

**Step 8: Test**
- Frontend: http://64.20.56.218/~pgtinter/
- Backend: http://64.20.56.218/~pgtinter/api/
- Login: admin / admin123

---

## 📦 WHAT TO UPLOAD

### Backend Files (to pgtinter/api/):
```
✅ main.py
✅ database.py
✅ models.py
✅ schemas.py
✅ auth.py
✅ crud.py
✅ modern_invoice_generator.py
✅ staff_ledger_generator.py
✅ invoice_service.py
✅ requirements.txt
✅ .env.production
✅ passenger_wsgi.py
✅ init_database.py
✅ ensure_admin.py
✅ All other .py files
```

### Frontend Files (to pgtinter/):
```
✅ index.html
✅ static/ folder (complete)
✅ manifest.json
✅ favicon.ico
✅ All files from build/
```

### Config Files:
```
✅ .htaccess (in pgtinter/)
✅ .htaccess (in pgtinter/api/)
```

---

## ⚠️ IMPORTANT NOTES

### Database Name Format:
- You create: `pgt_test_db`
- cPanel adds prefix: `pgtinter_pgt_test_db`
- Use full name in .env.production

### Python Dependencies:
If backend doesn't start, install dependencies:
```bash
cd public_html/pgtinter/api
pip3 install -r requirements.txt --user
```

### File Permissions:
- Folders: 755
- Files: 644
- Python files: 755 (if executable)

---

## 🧪 TESTING AFTER DEPLOYMENT

### 1. Test Frontend:
```
Open: http://64.20.56.218/~pgtinter/
Expected: Login page loads
```

### 2. Test Backend:
```
Open: http://64.20.56.218/~pgtinter/api/
Expected: {"message": "PGT TMS API"}
```

### 3. Test Login:
```
Username: admin
Password: admin123
Expected: Dashboard loads
```

### 4. Test Invoice:
```
Go to: Receivables
Click: Invoice button
Expected: PDF downloads with Red/Black theme
```

---

## 🎯 DIRECTOR'S AUDIT TESTS

Once deployed, perform these tests:

### Test 1: Hussain Stress Test
1. Login to http://64.20.56.218/~pgtinter/
2. Go to Staff Payroll
3. Find Muhammad Hussain
4. Generate statement
5. Verify: 140,000/- balance, running balance column, 28 months

### Test 2: Pak Afghan Aging
1. Go to Financial Ledgers
2. Select Pak Afghan
3. Generate report
4. Verify: Monthly grouping, 30-day highlighting in RED

### Test 3: Invoice Generation
1. Go to Receivables
2. Generate invoice
3. Verify: 412,500/- total, Red/Black theme, QR code

---

## 🚨 IF SOMETHING DOESN'T WORK

### Frontend shows blank page:
1. Check browser console (F12)
2. Verify .env.production has correct API_URL
3. Rebuild: `npm run build`
4. Re-upload build files

### Backend not responding:
1. Check cPanel error logs
2. Verify database credentials
3. Install dependencies: `pip3 install -r requirements.txt --user`
4. Restart Python app in cPanel

### Database connection error:
1. Verify database name: `pgtinter_pgt_test_db`
2. Check user has privileges
3. Test connection in cPanel → phpMyAdmin

---

## ✅ DEPLOYMENT COMPLETE WHEN:

- [ ] Frontend loads at http://64.20.56.218/~pgtinter/
- [ ] Can login with admin/admin123
- [ ] Dashboard displays
- [ ] Receivables page works
- [ ] Invoice generates with Red/Black theme
- [ ] Staff statements generate
- [ ] All calculations accurate

---

**Ready for Director's live audit!** 🎉


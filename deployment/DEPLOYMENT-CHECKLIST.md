# ✅ Deployment Checklist - PGT International TMS

## 📦 Pre-Deployment (On Your Local Machine)

### 1. Build Frontend
- [ ] Navigate to `frontend` folder
- [ ] Run `npm run build`
- [ ] Verify `build` folder created successfully
- [ ] Check build folder size (should be ~2-5 MB)

### 2. Prepare Files
- [ ] Verify `backend/pgt_tms.db` exists and has your data
- [ ] Check `backend/.env.production` has correct settings
- [ ] Verify `backend/passenger_wsgi.py` exists
- [ ] Check all deployment files in `deployment` folder

### 3. Test Locally One Last Time
- [ ] Login works (admin/admin123)
- [ ] Create a test trip
- [ ] Generate enhanced PDF report
- [ ] Verify all 4 international standards visible
- [ ] Test mobile form on phone

---

## 🌐 cPanel Setup

### 4. Login to cPanel
- [ ] Go to http://64.20.56.218:2082/
- [ ] Login: pgtinter / b@v]w8bIOU32O1
- [ ] Dashboard loads successfully

### 5. Create Subdomain
- [ ] Navigate to Domains → Subdomains
- [ ] Create subdomain: `tms`
- [ ] Domain: `pgtinternational.com`
- [ ] Document Root: `/home/pgtinter/public_html/tms`
- [ ] Subdomain created successfully

### 6. Setup Python Application
- [ ] Navigate to Software → Setup Python App
- [ ] Click Create Application
- [ ] Python Version: 3.9 or higher
- [ ] Application Root: `/home/pgtinter/tms-backend`
- [ ] Startup File: `passenger_wsgi.py`
- [ ] Entry Point: `application`
- [ ] Application created successfully

---

## 📤 File Upload (via FTP)

### 7. Connect to FTP
- [ ] Open FileZilla (or your FTP client)
- [ ] Host: pgtinternational.com
- [ ] Username: pgtinter
- [ ] Password: b@v]w8bIOU32O1
- [ ] Port: 21
- [ ] Connected successfully

### 8. Upload Backend Files
Upload to `/home/pgtinter/tms-backend/`:
- [ ] main.py
- [ ] models.py
- [ ] crud.py
- [ ] auth.py
- [ ] schemas.py
- [ ] database.py
- [ ] validators.py
- [ ] audit_service.py
- [ ] notification_service.py
- [ ] ledger_service.py
- [ ] ledger_engine.py
- [ ] financial_calculator.py
- [ ] report_generator.py
- [ ] enhanced_reports.py
- [ ] cash_register_service.py
- [ ] company_config.py
- [ ] ensure_admin.py
- [ ] reset_admin_password.py
- [ ] requirements.txt
- [ ] passenger_wsgi.py
- [ ] .env.production (rename to .env after upload)
- [ ] pgt_tms.db (YOUR DATABASE - IMPORTANT!)
- [ ] static/ folder (with logo files)

### 9. Upload Frontend Files
Upload contents of `frontend/build/` to `/home/pgtinter/public_html/tms/`:
- [ ] index.html
- [ ] static/ folder (css, js, media)
- [ ] manifest.json
- [ ] favicon.ico
- [ ] All other files from build folder

### 10. Upload Configuration Files
- [ ] Upload `deployment/.htaccess-frontend` as `/home/pgtinter/public_html/tms/.htaccess`
- [ ] Create folder `/home/pgtinter/public_html/tms/api/`
- [ ] Upload `deployment/.htaccess-api` as `/home/pgtinter/public_html/tms/api/.htaccess`
- [ ] Upload `deployment/cron-keepalive.sh` to `/home/pgtinter/tms-backend/`

---

## ⚙️ Configuration

### 11. Rename Environment File
- [ ] In FTP, navigate to `/home/pgtinter/tms-backend/`
- [ ] Rename `.env.production` to `.env`
- [ ] Edit `.env` and change SECRET_KEY to something unique

### 12. Set File Permissions
Via cPanel File Manager or FTP:
- [ ] Backend folder: 755
- [ ] Backend .py files: 644
- [ ] pgt_tms.db: 664
- [ ] cron-keepalive.sh: 755 (executable)
- [ ] Frontend folder: 755
- [ ] Frontend files: 644
- [ ] .htaccess files: 644

### 13. Install Python Dependencies
- [ ] In cPanel → Setup Python App
- [ ] Click on your application
- [ ] Click "Run Pip Install"
- [ ] Wait for completion (may take 2-5 minutes)
- [ ] Verify no errors in logs

---

## 🚀 Launch

### 14. Start Backend
- [ ] In cPanel → Setup Python App
- [ ] Click on your application
- [ ] Click "Restart" button
- [ ] Status shows "Running"
- [ ] Check logs for any errors

### 15. Setup Cron Job
- [ ] Navigate to Advanced → Cron Jobs
- [ ] Add new cron job:
  - Minute: `*/5`
  - Hour: `*`
  - Day: `*`
  - Month: `*`
  - Weekday: `*`
  - Command: `/home/pgtinter/tms-backend/cron-keepalive.sh`
- [ ] Cron job created successfully

### 16. Install SSL Certificate
- [ ] Navigate to Security → SSL/TLS Status
- [ ] Find `tms.pgtinternational.com`
- [ ] Click "Run AutoSSL"
- [ ] Wait 2-5 minutes
- [ ] Status shows "Certificate installed"
- [ ] HTTPS working

---

## 🧪 Testing

### 17. Test Frontend
- [ ] Open browser: https://tms.pgtinternational.com
- [ ] Login page loads correctly
- [ ] No console errors (F12)
- [ ] PGT branding visible

### 18. Test Backend API
- [ ] Open browser: https://tms.pgtinternational.com/api/docs
- [ ] FastAPI documentation loads
- [ ] All endpoints visible

### 19. Test Login
- [ ] Login with: admin / admin123
- [ ] Dashboard loads successfully
- [ ] All menu items visible
- [ ] No errors in console

### 20. Test Core Features
- [ ] View Fleet Logs (existing trips visible)
- [ ] View Clients (Pak Afghan visible)
- [ ] View Vendors (all vendors visible)
- [ ] View Staff Payroll (Muhammad Hussain visible)
- [ ] View Receivable Aging (4.9M visible)

### 21. Test Enhanced Reports
- [ ] Go to Vendors → Pak Afghan
- [ ] Click "Download Ledger PDF"
- [ ] PDF downloads successfully
- [ ] Verify Quick Info Box (top right)
- [ ] Verify Monthly Grouping
- [ ] Verify Color-Coded Status
- [ ] Verify PGT Letterhead

### 22. Test Financial Summary
- [ ] Go to Reports → Financial Summary
- [ ] Click "Download PDF"
- [ ] PDF downloads successfully
- [ ] Verify Expense Breakdown
- [ ] Verify Receivable Aging Table
- [ ] Verify 4.9M from Pak Afghan visible

### 23. Test Staff Statement
- [ ] Go to Staff Payroll → Muhammad Hussain
- [ ] Click "View Ledger"
- [ ] Click "Print Statement"
- [ ] PDF downloads successfully
- [ ] Verify Quick Info Box
- [ ] Verify 140,000 advance visible
- [ ] Verify 10,000/month deduction

### 24. Test Mobile Form
- [ ] Open on phone: https://tms.pgtinternational.com/supervisor-mobile
- [ ] Login with: supervisor / supervisor123
- [ ] Form loads correctly
- [ ] Dropdowns work
- [ ] Camera button works
- [ ] Can capture photo
- [ ] Can submit trip

### 25. Test Role-Based Access
- [ ] Login as Manager (manager/manager123)
- [ ] Verify NO profit columns visible in Fleet Logs
- [ ] Login as Supervisor (supervisor/supervisor123)
- [ ] Verify NO freight or profit visible
- [ ] Login as Admin (admin/admin123)
- [ ] Verify ALL columns visible

---

## 🔐 Security

### 26. Change Default Passwords
- [ ] Change admin password from admin123
- [ ] Change manager password from manager123
- [ ] Change supervisor password from supervisor123
- [ ] Document new passwords securely

### 27. Update SECRET_KEY
- [ ] Edit `/home/pgtinter/tms-backend/.env`
- [ ] Change SECRET_KEY to unique random string
- [ ] Save file
- [ ] Restart backend application

### 28. Configure Firewall
- [ ] In cPanel → Security → IP Blocker
- [ ] Consider restricting access to specific IPs
- [ ] Enable ModSecurity if available

---

## 📊 Post-Deployment

### 29. Setup Backups
- [ ] Download pgt_tms.db to local machine
- [ ] Use "Export All Data" in Settings
- [ ] Schedule weekly backups
- [ ] Store backups in safe location

### 30. Monitor Performance
- [ ] Check cPanel resource usage
- [ ] Review error logs daily
- [ ] Monitor API response times
- [ ] Check disk space usage

### 31. Documentation
- [ ] Share URLs with team
- [ ] Document any custom changes
- [ ] Update credentials document
- [ ] Create user training materials

### 32. Inform Stakeholders
- [ ] Notify Director deployment is complete
- [ ] Share login credentials securely
- [ ] Provide user guide
- [ ] Schedule training session

---

## 🎯 Success Criteria

Your deployment is successful when:
- ✅ Frontend loads at https://tms.pgtinternational.com
- ✅ API docs load at https://tms.pgtinternational.com/api/docs
- ✅ Login works with all 3 roles
- ✅ Enhanced reports download with all 4 international standards
- ✅ Mobile form works on phone
- ✅ Role-based access control working (Manager sees no profit)
- ✅ SSL certificate installed (HTTPS working)
- ✅ Backend stays running (cron job working)
- ✅ All existing data visible (trips, clients, vendors, staff)
- ✅ No console errors in browser

---

## 📞 Emergency Contacts

**Hosting Support:** Contact your hosting provider  
**cPanel Issues:** Check cPanel documentation  
**App Issues:** Review logs in cPanel → Setup Python App → Logs

---

## 🔄 Rollback Plan

If deployment fails:
1. Keep local version running
2. Download database from server
3. Review error logs
4. Fix issues locally
5. Re-deploy

---

**Deployment Date:** _______________  
**Deployed By:** _______________  
**Verified By:** _______________  
**Director Approval:** _______________

---

**Live URL:** https://tms.pgtinternational.com  
**API URL:** https://tms.pgtinternational.com/api  
**Mobile URL:** https://tms.pgtinternational.com/supervisor-mobile

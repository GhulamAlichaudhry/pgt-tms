# 🚀 Quick Deployment Steps for cPanel

## Prerequisites
- cPanel login: http://64.20.56.218:2082/
- Username: pgtinter
- Password: b@v]w8bIOU32O1
- FTP client (FileZilla recommended)

---

## STEP 1: Build Frontend (On Your Local Machine)

```bash
cd frontend
npm run build
```

This creates a `build` folder with production-ready files.

---

## STEP 2: Login to cPanel

1. Go to: http://64.20.56.218:2082/
2. Login with credentials above
3. You'll see the cPanel dashboard

---

## STEP 3: Create Subdomain

1. In cPanel, find **Domains** section
2. Click **Subdomains**
3. Fill in:
   - Subdomain: `tms`
   - Domain: `pgtinternational.com`
   - Document Root: `/home/pgtinter/public_html/tms`
4. Click **Create**

---

## STEP 4: Setup Python Application

1. In cPanel, find **Software** section
2. Click **Setup Python App**
3. Click **Create Application**
4. Configure:
   - Python Version: **3.9** (or latest available)
   - Application Root: `/home/pgtinter/tms-backend`
   - Application URL: Leave blank (we'll use reverse proxy)
   - Application Startup File: `passenger_wsgi.py`
   - Application Entry Point: `application`
5. Click **Create**

---

## STEP 5: Upload Files via FTP

### Connect to FTP:
- Host: `pgtinternational.com` or `64.20.56.218`
- Username: `pgtinter`
- Password: `b@v]w8bIOU32O1`
- Port: `21`

### Upload Backend Files:
Upload entire `backend` folder contents to:
```
/home/pgtinter/tms-backend/
```

Include:
- All .py files
- requirements.txt
- pgt_tms.db (your database)
- .env.production
- passenger_wsgi.py
- static/ folder

### Upload Frontend Files:
Upload contents of `frontend/build` folder to:
```
/home/pgtinter/public_html/tms/
```

Include:
- index.html
- static/ folder
- All other files from build folder

### Upload .htaccess Files:

1. Upload `deployment/.htaccess-frontend` to:
   ```
   /home/pgtinter/public_html/tms/.htaccess
   ```

2. Create folder `/home/pgtinter/public_html/tms/api/`

3. Upload `deployment/.htaccess-api` to:
   ```
   /home/pgtinter/public_html/tms/api/.htaccess
   ```

---

## STEP 6: Install Python Dependencies

1. In cPanel, go to **Setup Python App**
2. Click on your `tms-backend` application
3. Scroll to **Configuration Files**
4. Click **Run Pip Install**
5. Wait for installation to complete

Or use Terminal in cPanel:
```bash
cd /home/pgtinter/tms-backend
source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate
pip install -r requirements.txt
```

---

## STEP 7: Configure Environment

1. In FTP, navigate to `/home/pgtinter/tms-backend/`
2. Rename `.env.production` to `.env`
3. Edit `.env` and change the SECRET_KEY to something unique

---

## STEP 8: Start Backend Application

### Option A: Using cPanel Python App Manager
1. Go to **Setup Python App**
2. Click on your application
3. Click **Restart** button
4. Status should show "Running"

### Option B: Using Terminal
```bash
cd /home/pgtinter/tms-backend
source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate
python ensure_admin.py
uvicorn main:app --host 0.0.0.0 --port 8002 &
```

---

## STEP 9: Setup Auto-Restart (Cron Job)

1. In cPanel, go to **Advanced** → **Cron Jobs**
2. Add new cron job:
   - **Minute:** `*/5` (every 5 minutes)
   - **Hour:** `*`
   - **Day:** `*`
   - **Month:** `*`
   - **Weekday:** `*`
   - **Command:**
   ```bash
   /home/pgtinter/tms-backend/cron-keepalive.sh
   ```
3. Click **Add New Cron Job**

First, upload `deployment/cron-keepalive.sh` to `/home/pgtinter/tms-backend/`

Make it executable via Terminal:
```bash
chmod +x /home/pgtinter/tms-backend/cron-keepalive.sh
```

---

## STEP 10: Install SSL Certificate

1. In cPanel, go to **Security** → **SSL/TLS Status**
2. Find `tms.pgtinternational.com`
3. Click **Run AutoSSL**
4. Wait 2-5 minutes for certificate installation
5. Status should show "AutoSSL certificate installed"

---

## STEP 11: Test Your Deployment

### Test Frontend:
Open browser: `https://tms.pgtinternational.com`

You should see the login page.

### Test Backend API:
Open browser: `https://tms.pgtinternational.com/api/docs`

You should see FastAPI documentation.

### Test Login:
- Username: `admin`
- Password: `admin123`

---

## STEP 12: Verify Enhanced Reports

After logging in, test the enhanced reports:

1. Go to Vendors page
2. Click on "Pak Afghan"
3. Click "Download Ledger PDF"
4. Verify it has:
   - Quick Info Box (top right)
   - Monthly grouping
   - Color-coded status
   - PGT letterhead

---

## 🔧 Troubleshooting

### Frontend shows blank page:
1. Check browser console (F12) for errors
2. Verify .htaccess file exists in `/home/pgtinter/public_html/tms/`
3. Check file permissions (755 for folders, 644 for files)

### API not responding:
1. Check if backend is running in cPanel → Setup Python App
2. Check error logs in cPanel → Setup Python App → Logs
3. Verify port 8002 is not blocked

### Database errors:
1. Ensure `pgt_tms.db` was uploaded
2. Check file permissions (664)
3. Run `python ensure_admin.py` via Terminal

### Login not working:
1. Via Terminal, run:
   ```bash
   cd /home/pgtinter/tms-backend
   source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate
   python reset_admin_password.py
   ```
2. Try login again with admin/admin123

---

## 📱 Mobile Access

Supervisors can access mobile form at:
`https://tms.pgtinternational.com/supervisor-mobile`

---

## 🔐 Security Checklist

- [ ] Changed SECRET_KEY in .env
- [ ] SSL certificate installed (HTTPS working)
- [ ] Changed default admin password
- [ ] Firewall rules configured in cPanel
- [ ] Regular backups scheduled

---

## 📞 Support Resources

**cPanel Documentation:** https://docs.cpanel.net/  
**FastAPI Deployment:** https://fastapi.tiangolo.com/deployment/  
**Your Hosting Support:** Contact your hosting provider

---

## 🎯 Post-Deployment Tasks

1. **Test all features:**
   - Login with all 3 roles
   - Create test trip
   - Generate reports
   - Test mobile form

2. **Setup backups:**
   - Download database weekly
   - Use "Export All Data" in Settings
   - Keep local backup

3. **Monitor performance:**
   - Check cPanel resource usage
   - Review error logs daily
   - Monitor API response times

4. **Update documentation:**
   - Share URLs with team
   - Document any custom changes
   - Keep credentials secure

---

**Deployment Date:** February 23, 2026  
**Live URL:** https://tms.pgtinternational.com  
**API URL:** https://tms.pgtinternational.com/api

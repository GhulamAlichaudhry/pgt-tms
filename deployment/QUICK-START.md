# 🚀 Quick Start - Deploy to cPanel in 30 Minutes

## Your Hosting Info
- **cPanel:** http://64.20.56.218:2082/
- **Login:** pgtinter / b@v]w8bIOU32O1
- **Domain:** pgtinternational.com
- **Subdomain:** tms.pgtinternational.com

---

## Step 1: Build Frontend (5 min)

On your local machine:
```bash
cd frontend
npm run build
```

Wait for build to complete. You'll see a `build` folder.

---

## Step 2: Login to cPanel (2 min)

1. Open: http://64.20.56.218:2082/
2. Login with credentials above
3. You're in!

---

## Step 3: Create Subdomain (3 min)

1. Find **Domains** → **Subdomains**
2. Create:
   - Subdomain: `tms`
   - Domain: `pgtinternational.com`
3. Click **Create**

---

## Step 4: Setup Python App (3 min)

1. Find **Software** → **Setup Python App**
2. Click **Create Application**
3. Fill:
   - Python: 3.9
   - Root: `/home/pgtinter/tms-backend`
   - Startup: `passenger_wsgi.py`
   - Entry: `application`
4. Click **Create**

---

## Step 5: Upload Files via FTP (10 min)

### Connect FTP:
- Host: `pgtinternational.com`
- User: `pgtinter`
- Pass: `b@v]w8bIOU32O1`

### Upload Backend:
Drag entire `backend` folder to `/home/pgtinter/tms-backend/`

### Upload Frontend:
Drag contents of `frontend/build/` to `/home/pgtinter/public_html/tms/`

### Upload Config Files:
1. `deployment/.htaccess-frontend` → `/home/pgtinter/public_html/tms/.htaccess`
2. Create folder: `/home/pgtinter/public_html/tms/api/`
3. `deployment/.htaccess-api` → `/home/pgtinter/public_html/tms/api/.htaccess`

---

## Step 6: Configure (2 min)

1. Rename `/home/pgtinter/tms-backend/.env.production` to `.env`
2. Done!

---

## Step 7: Install Dependencies (3 min)

1. cPanel → **Setup Python App**
2. Click your app
3. Click **Run Pip Install**
4. Wait...

---

## Step 8: Start Backend (1 min)

1. cPanel → **Setup Python App**
2. Click **Restart**
3. Status: "Running" ✅

---

## Step 9: Install SSL (2 min)

1. cPanel → **Security** → **SSL/TLS Status**
2. Find `tms.pgtinternational.com`
3. Click **Run AutoSSL**
4. Wait...

---

## Step 10: Test! (5 min)

Open: https://tms.pgtinternational.com

Login:
- Username: `admin`
- Password: `admin123`

Test:
1. Dashboard loads ✅
2. View Fleet Logs ✅
3. Download enhanced PDF ✅
4. Check for 4 international standards ✅

---

## 🎉 You're Live!

**Frontend:** https://tms.pgtinternational.com  
**API:** https://tms.pgtinternational.com/api/docs  
**Mobile:** https://tms.pgtinternational.com/supervisor-mobile

---

## 🆘 Quick Fixes

### Login not working?
```bash
# Via cPanel Terminal:
cd /home/pgtinter/tms-backend
source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate
python reset_admin_password.py
```

### Backend not running?
1. cPanel → Setup Python App
2. Click your app
3. Click **Restart**

### Frontend blank page?
1. Check .htaccess exists in `/home/pgtinter/public_html/tms/`
2. Clear browser cache
3. Try incognito mode

---

## 📋 Full Documentation

For detailed steps, see:
- `deployment/DEPLOYMENT-STEPS.md`
- `deployment/DEPLOYMENT-CHECKLIST.md`
- `CPANEL-DEPLOYMENT-GUIDE.md`

---

**Need Help?** Check error logs in cPanel → Setup Python App → Logs

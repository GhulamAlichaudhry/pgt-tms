# 🚀 cPanel Deployment Guide - PGT International TMS

## 📋 Your Hosting Details

**Domain:** pgtinternational.com  
**Server IP:** 64.20.56.218  
**cPanel URL:** http://64.20.56.218:2082/  
**Username:** pgtinter  
**Password:** b@v]w8bIOU32O1

**Nameservers:**
- cpns1.mypremiumdns.com (64.20.56.218)
- cpns2.mypremiumdns.com (64.20.56.218)

---

## 🎯 Deployment Strategy

We'll deploy the app on a subdomain: **tms.pgtinternational.com**

**Architecture:**
- Frontend: `tms.pgtinternational.com` (React app)
- Backend API: `tms.pgtinternational.com/api` (Python FastAPI)

---

## 📝 Step-by-Step Deployment

### STEP 1: Create Subdomain in cPanel

1. Login to cPanel: http://64.20.56.218:2082/
2. Navigate to **Domains** → **Subdomains**
3. Create new subdomain:
   - **Subdomain:** `tms`
   - **Domain:** `pgtinternational.com`
   - **Document Root:** `/home/pgtinter/public_html/tms`
4. Click **Create**

---

### STEP 2: Setup Python Application in cPanel

1. In cPanel, go to **Software** → **Setup Python App**
2. Click **Create Application**
3. Configure:
   - **Python Version:** 3.9 or higher
   - **Application Root:** `/home/pgtinter/tms-backend`
   - **Application URL:** `tms.pgtinternational.com/api`
   - **Application Startup File:** `main.py`
   - **Application Entry Point:** `app`
4. Click **Create**

---

### STEP 3: Upload Backend Files via FTP

**FTP Details:**
- **Host:** pgtinternational.com (or 64.20.56.218)
- **Username:** pgtinter
- **Password:** b@v]w8bIOU32O1
- **Port:** 21

**Files to Upload:**
Upload entire `backend` folder to `/home/pgtinter/tms-backend/`

**Required Files:**
```
/home/pgtinter/tms-backend/
├── main.py
├── models.py
├── crud.py
├── auth.py
├── schemas.py
├── database.py
├── validators.py
├── audit_service.py
├── notification_service.py
├── ledger_service.py
├── ledger_engine.py
├── financial_calculator.py
├── report_generator.py
├── enhanced_reports.py
├── cash_register_service.py
├── company_config.py
├── ensure_admin.py
├── requirements.txt
├── pgt_tms.db (your database)
└── static/
    └── (logo files)
```

---

### STEP 4: Install Python Dependencies

1. In cPanel, go to **Setup Python App**
2. Click on your application
3. Scroll to **Configuration Files**
4. Click **Edit** on `requirements.txt`
5. Or use SSH/Terminal to run:
```bash
cd /home/pgtinter/tms-backend
source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate
pip install -r requirements.txt
```

**Key Dependencies:**
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
reportlab==4.0.7
openpyxl==3.1.2
```

---

### STEP 5: Configure Backend for Production

Create `.env` file in `/home/pgtinter/tms-backend/`:

```env
# Database
DATABASE_URL=sqlite:///./pgt_tms.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS - Allow frontend domain
ALLOWED_ORIGINS=https://tms.pgtinternational.com,http://tms.pgtinternational.com

# Server
HOST=0.0.0.0
PORT=8002
```

---

### STEP 6: Build Frontend for Production

On your local machine:

```bash
cd frontend

# Update .env.production
echo "REACT_APP_API_URL=https://tms.pgtinternational.com/api" > .env.production

# Build production version
npm run build
```

This creates a `build` folder with optimized static files.

---

### STEP 7: Upload Frontend Files

Upload contents of `frontend/build` folder to `/home/pgtinter/public_html/tms/`

**Structure:**
```
/home/pgtinter/public_html/tms/
├── index.html
├── static/
│   ├── css/
│   ├── js/
│   └── media/
├── manifest.json
└── favicon.ico
```

---

### STEP 8: Configure .htaccess for React Router

Create `/home/pgtinter/public_html/tms/.htaccess`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteCond %{REQUEST_FILENAME} !-l
  RewriteRule . /index.html [L]
</IfModule>

# Enable CORS
<IfModule mod_headers.c>
  Header set Access-Control-Allow-Origin "*"
  Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
  Header set Access-Control-Allow-Headers "Content-Type, Authorization"
</IfModule>

# Compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/json
</IfModule>

# Browser Caching
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

---

### STEP 9: Setup Reverse Proxy for API

Create `/home/pgtinter/public_html/tms/api/.htaccess`:

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule ^(.*)$ http://127.0.0.1:8002/$1 [P,L]
</IfModule>

<IfModule mod_headers.c>
  Header set Access-Control-Allow-Origin "*"
  Header set Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
  Header set Access-Control-Allow-Headers "Content-Type, Authorization"
</IfModule>
```

---

### STEP 10: Start Backend Application

1. In cPanel, go to **Setup Python App**
2. Click on your application
3. Click **Start** or **Restart**
4. Verify status shows "Running"

Or via SSH:
```bash
cd /home/pgtinter/tms-backend
source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate
python main.py
```

---

### STEP 11: Setup Auto-Start (Keep Backend Running)

Create a startup script in cPanel:

1. Go to **Advanced** → **Cron Jobs**
2. Add new cron job:
   - **Minute:** `*/5` (every 5 minutes)
   - **Command:**
   ```bash
   cd /home/pgtinter/tms-backend && source /home/pgtinter/virtualenv/tms-backend/3.9/bin/activate && python ensure_admin.py && nohup python main.py > /dev/null 2>&1 &
   ```

This ensures the backend restarts if it crashes.

---

### STEP 12: SSL Certificate (HTTPS)

1. In cPanel, go to **Security** → **SSL/TLS Status**
2. Find `tms.pgtinternational.com`
3. Click **Run AutoSSL**
4. Wait for certificate installation

This enables HTTPS for secure connections.

---

## 🔧 Alternative: Using Passenger (Recommended for cPanel)

If your cPanel has Passenger support:

1. Create `passenger_wsgi.py` in `/home/pgtinter/tms-backend/`:

```python
import sys
import os

# Add application directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import FastAPI app
from main import app as application

# Passenger expects 'application' variable
```

2. Create `.htaccess` in `/home/pgtinter/public_html/tms/`:

```apache
PassengerEnabled On
PassengerAppRoot /home/pgtinter/tms-backend
PassengerBaseURI /api
PassengerPython /home/pgtinter/virtualenv/tms-backend/3.9/bin/python
```

---

## 🌐 Access URLs After Deployment

**Frontend:** https://tms.pgtinternational.com  
**Backend API:** https://tms.pgtinternational.com/api  
**API Docs:** https://tms.pgtinternational.com/api/docs

**Login Credentials:**
- Admin: admin / admin123
- Manager: manager / manager123
- Supervisor: supervisor / supervisor123

---

## 📱 Mobile Access

Supervisors can access the mobile form at:
**https://tms.pgtinternational.com/supervisor-mobile**

---

## 🔍 Troubleshooting

### Backend Not Starting
1. Check Python version: `python --version` (need 3.9+)
2. Check logs in cPanel → Setup Python App → View Logs
3. Verify all dependencies installed: `pip list`

### Frontend Shows Blank Page
1. Check browser console for errors (F12)
2. Verify .htaccess file exists
3. Check file permissions (755 for folders, 644 for files)

### API Connection Failed
1. Verify backend is running in cPanel
2. Check CORS settings in backend
3. Test API directly: https://tms.pgtinternational.com/api/docs

### Database Issues
1. Ensure `pgt_tms.db` uploaded correctly
2. Check file permissions (664)
3. Run `ensure_admin.py` to reset credentials

---

## 📦 Quick Deployment Checklist

- [ ] Create subdomain `tms.pgtinternational.com`
- [ ] Setup Python app in cPanel
- [ ] Upload backend files via FTP
- [ ] Install Python dependencies
- [ ] Create .env file with production settings
- [ ] Build frontend (`npm run build`)
- [ ] Upload frontend build files
- [ ] Create .htaccess files
- [ ] Start backend application
- [ ] Setup cron job for auto-restart
- [ ] Install SSL certificate
- [ ] Test login at https://tms.pgtinternational.com
- [ ] Test API at https://tms.pgtinternational.com/api/docs
- [ ] Verify enhanced reports work
- [ ] Test mobile form on phone

---

## 🎯 Next Steps After Deployment

1. **Test All Features:**
   - Login with all 3 roles
   - Create a test trip
   - Generate enhanced reports
   - Test mobile form on phone

2. **Backup Strategy:**
   - Download database weekly: `pgt_tms.db`
   - Use "Export All Data" button in Settings
   - Keep local backup of all files

3. **Monitor Performance:**
   - Check cPanel resource usage
   - Monitor API response times
   - Review error logs regularly

4. **Security:**
   - Change default passwords
   - Update SECRET_KEY in .env
   - Enable firewall rules in cPanel
   - Keep Python packages updated

---

## 📞 Support

**cPanel Support:** Contact your hosting provider  
**App Issues:** Check logs in cPanel → Setup Python App → Logs  
**Database Backup:** Download from `/home/pgtinter/tms-backend/pgt_tms.db`

---

**Deployment Date:** February 23, 2026  
**App Version:** 1.0 (International Standards Edition)  
**Domain:** tms.pgtinternational.com

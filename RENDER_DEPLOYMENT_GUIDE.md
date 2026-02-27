# 🚀 RENDER.COM FREE DEPLOYMENT GUIDE

## 🎯 DEPLOY PGT TMS TO RENDER.COM (FREE)

**Target:** Free Render.com hosting  
**Time:** 15-20 minutes  
**Cost:** $0 (100% FREE)  
**Result:** Live system with custom URL  

---

## ✅ WHAT YOU'LL GET

**Backend URL:** `https://pgt-tms-backend.onrender.com`  
**Frontend URL:** `https://pgt-tms-frontend.onrender.com`  
**Database:** PostgreSQL (Free tier - 1GB)  
**HTTPS:** Included automatically  
**Uptime:** Free tier spins down after 15 min inactivity (wakes up in 30 sec)  

---

## 📋 PREREQUISITES

### Before You Start:
- [ ] GitHub account (free)
- [ ] Render.com account (free - sign up with GitHub)
- [ ] Git installed on your computer
- [ ] 15-20 minutes of time

---

## 🚀 DEPLOYMENT STEPS

### STEP 1: Create GitHub Repository (5 min)

**1.1 Create Repository on GitHub:**
1. Go to https://github.com
2. Click "New repository"
3. Name: `pgt-tms`
4. Description: "PGT International Transport Management System"
5. Visibility: Private (recommended) or Public
6. Click "Create repository"

**1.2 Push Your Code to GitHub:**

Open PowerShell/Terminal in your project folder:

```powershell
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - PGT TMS ready for Render deployment"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/pgt-tms.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Expected:** Your code is now on GitHub!

---

### STEP 2: Sign Up for Render.com (2 min)

**2.1 Create Account:**
1. Go to https://render.com
2. Click "Get Started"
3. Click "Sign up with GitHub"
4. Authorize Render to access your GitHub
5. Complete profile setup

**Expected:** You're logged into Render dashboard

---

### STEP 3: Deploy Backend (5 min)

**3.1 Create Web Service:**
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Click "Connect a repository"
4. Find and select your `pgt-tms` repository
5. Click "Connect"

**3.2 Configure Backend Service:**

Fill in these settings:

**Basic Settings:**
- **Name:** `pgt-tms-backend`
- **Region:** Oregon (US West) - or closest to you
- **Branch:** `main`
- **Root Directory:** `backend`
- **Environment:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings:**
- **Plan:** Free
- **Auto-Deploy:** Yes

**3.3 Add Environment Variables:**

Click "Advanced" → "Add Environment Variable"

Add these variables:

```
SECRET_KEY = [Click "Generate" button]
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ENVIRONMENT = production
DEBUG = False
COMPANY_NAME = PGT International (Private) Limited
COMPANY_NTN = 7654321-0
COMPANY_PHONE = 0300-1210706
COMPANY_MOBILE = 0321-9876543
COMPANY_EMAIL = info@pgtinternational.com
COMPANY_ADDRESS = Main GT Road, Sahiwal, Punjab, Pakistan
```

**3.4 Create Database:**

1. Scroll down to "Add Database"
2. Click "New Database"
3. Select "PostgreSQL"
4. Name: `pgt-tms-db`
5. Database Name: `pgt_tms`
6. Plan: Free
7. Click "Create Database"

**Note:** Render will automatically add `DATABASE_URL` environment variable

**3.5 Deploy:**

1. Click "Create Web Service"
2. Wait for deployment (3-5 minutes)
3. Watch the logs for any errors

**Expected:** Backend deploys successfully!

**Your Backend URL:** `https://pgt-tms-backend.onrender.com`

---

### STEP 4: Initialize Database (2 min)

**4.1 Run Database Initialization:**

After backend is deployed:

1. In Render dashboard, go to your `pgt-tms-backend` service
2. Click "Shell" tab (top right)
3. Run these commands:

```bash
python init_database.py
python ensure_admin.py
```

**Expected Output:**
```
✅ Database initialized successfully
✅ Admin user created: admin / admin123
```

**4.2 Test Backend:**

Open in browser:
```
https://pgt-tms-backend.onrender.com/
```

**Expected:** JSON response with API status

---

### STEP 5: Deploy Frontend (5 min)

**5.1 Update Frontend Environment:**

Before deploying frontend, update the API URL:

1. Open `frontend/.env.render`
2. Update with your actual backend URL:

```env
REACT_APP_API_URL=https://pgt-tms-backend.onrender.com
REACT_APP_ENVIRONMENT=production
REACT_APP_COMPANY_NAME=PGT International (Private) Limited
```

3. Commit and push:

```powershell
git add frontend/.env.render
git commit -m "Update frontend API URL"
git push
```

**5.2 Create Static Site:**

1. In Render dashboard, click "New +"
2. Select "Static Site"
3. Select your `pgt-tms` repository
4. Click "Connect"

**5.3 Configure Frontend Service:**

Fill in these settings:

**Basic Settings:**
- **Name:** `pgt-tms-frontend`
- **Branch:** `main`
- **Root Directory:** `frontend`
- **Build Command:** `npm install && npm run build`
- **Publish Directory:** `build`

**Environment Variables:**

Click "Advanced" → "Add Environment Variable"

```
REACT_APP_API_URL = https://pgt-tms-backend.onrender.com
REACT_APP_ENVIRONMENT = production
REACT_APP_COMPANY_NAME = PGT International (Private) Limited
```

**5.4 Deploy:**

1. Click "Create Static Site"
2. Wait for deployment (3-5 minutes)
3. Watch the logs

**Expected:** Frontend deploys successfully!

**Your Frontend URL:** `https://pgt-tms-frontend.onrender.com`

---

### STEP 6: Update CORS Settings (2 min)

**6.1 Update Backend CORS:**

1. Go to your backend service in Render
2. Click "Environment"
3. Add/Update environment variable:

```
ALLOWED_ORIGINS = https://pgt-tms-frontend.onrender.com
```

4. Click "Save Changes"
5. Backend will automatically redeploy

---

### STEP 7: Test Your Deployment (3 min)

**7.1 Test Frontend:**

1. Open: `https://pgt-tms-frontend.onrender.com`
2. Expected: Login page loads
3. Login: `admin` / `admin123`
4. Expected: Dashboard loads

**7.2 Test Features:**

- [ ] Dashboard displays
- [ ] Fleet Logs page loads
- [ ] Receivables page loads
- [ ] Can navigate all pages

**7.3 Test Invoice Generation:**

1. Go to Receivables
2. Click "Generate Invoice"
3. Expected: PDF downloads with Red/Black theme

**7.4 Test Statement Generation:**

1. Go to Staff Payroll
2. Generate statement
3. Expected: PDF downloads with running balance

---

## ✅ DEPLOYMENT COMPLETE!

**Your Live URLs:**

**Frontend (Main App):**
```
https://pgt-tms-frontend.onrender.com
```

**Backend (API):**
```
https://pgt-tms-backend.onrender.com
```

**Login Credentials:**
```
Username: admin
Password: admin123
```

---

## 🎯 DIRECTOR'S AUDIT TESTS

### Test 1: Hussain Stress Test
1. Login to your Render URL
2. Navigate to Staff Payroll
3. Generate Muhammad Hussain statement
4. Verify: PKR 140,000/- balance with running balance

### Test 2: Invoice Generation
1. Navigate to Receivables
2. Generate invoice
3. Verify: PKR 412,500/- total with Red/Black theme

### Test 3: Pak Afghan Aging
1. Navigate to Financial Ledgers
2. Generate Pak Afghan report
3. Verify: 30+ day balances highlighted in RED

---

## 🚨 TROUBLESHOOTING

### Issue: Backend deployment fails

**Check:**
1. Render logs for errors
2. Verify requirements.txt is correct
3. Check Python version (should be 3.9+)

**Solution:**
```bash
# In Render Shell
pip install -r requirements.txt
python init_database.py
```

---

### Issue: Frontend shows blank page

**Check:**
1. Browser console (F12) for errors
2. Verify API URL in environment variables
3. Check CORS settings

**Solution:**
1. Update ALLOWED_ORIGINS in backend
2. Redeploy frontend with correct API_URL

---

### Issue: Database connection error

**Check:**
1. Verify DATABASE_URL is set automatically by Render
2. Check database is created and running

**Solution:**
1. Go to Render dashboard → Databases
2. Verify pgt-tms-db is running
3. Check connection string is added to backend

---

### Issue: App spins down (free tier)

**Behavior:**
- Free tier apps spin down after 15 minutes of inactivity
- Takes 30 seconds to wake up on first request

**Solution:**
- This is normal for free tier
- Upgrade to paid plan ($7/month) for always-on
- Or use a ping service to keep it alive

---

## 💡 IMPORTANT NOTES

### Free Tier Limitations:

**Backend:**
- 512 MB RAM
- Spins down after 15 min inactivity
- 750 hours/month (enough for testing)
- Wakes up in ~30 seconds

**Frontend:**
- 100 GB bandwidth/month
- Always on (static sites don't spin down)
- Custom domain supported

**Database:**
- 1 GB storage
- Expires after 90 days (can create new one)
- Automatic backups not included

### Upgrading:

If you need more:
- **Starter Plan:** $7/month (always on, more resources)
- **Standard Plan:** $25/month (production ready)

---

## 🎊 ADVANTAGES OF RENDER.COM

✅ **100% Free** for testing  
✅ **HTTPS included** automatically  
✅ **PostgreSQL database** included  
✅ **Auto-deploy** from GitHub  
✅ **Easy to use** dashboard  
✅ **No credit card** required for free tier  
✅ **Custom domains** supported  
✅ **Environment variables** management  
✅ **Logs and monitoring** included  

---

## 📊 DEPLOYMENT SUMMARY

**Time Taken:** 15-20 minutes  
**Cost:** $0 (FREE)  
**Services Created:**
- ✅ Backend Web Service
- ✅ Frontend Static Site
- ✅ PostgreSQL Database

**URLs:**
- Frontend: `https://pgt-tms-frontend.onrender.com`
- Backend: `https://pgt-tms-backend.onrender.com`

**Status:** LIVE AND OPERATIONAL ✅

---

## 🔄 UPDATING YOUR DEPLOYMENT

### To Update Code:

```powershell
# Make your changes
git add .
git commit -m "Your update message"
git push

# Render will auto-deploy!
```

### To Update Environment Variables:

1. Go to Render dashboard
2. Select your service
3. Click "Environment"
4. Update variables
5. Click "Save Changes"
6. Service will redeploy automatically

---

## 📞 SUPPORT

### Render Documentation:
- https://render.com/docs
- https://render.com/docs/deploy-fastapi
- https://render.com/docs/deploy-create-react-app

### Common Issues:
- Check Render logs for errors
- Verify environment variables
- Check database connection
- Verify CORS settings

---

## 🎉 SUCCESS!

**Your PGT International TMS is now live on Render.com!**

**Share your URL:**
```
https://pgt-tms-frontend.onrender.com
```

**Login and test:**
- Username: admin
- Password: admin123

**Run Director's audit tests and verify everything works!**

---

## 📝 NEXT STEPS

### After Successful Deployment:

1. **Test thoroughly** - Run all 3 audit tests
2. **Share URL** - Send to Director for review
3. **Gather feedback** - Note any issues or improvements
4. **Plan production** - Consider paid plan for production use
5. **Custom domain** - Add your own domain (optional)

### For Production:

1. **Upgrade plan** - $7/month for always-on
2. **Add custom domain** - tms.pgtinternational.com
3. **Enable backups** - Database backup strategy
4. **Monitor usage** - Check logs and metrics
5. **Security** - Update passwords, enable 2FA

---

**DEPLOYMENT COMPLETE!** 🚀  
**YOUR APP IS LIVE!** 🎉

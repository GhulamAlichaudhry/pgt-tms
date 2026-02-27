# 🚀 DEPLOY TO RENDER.COM NOW!

## ⚡ 3 STEPS - 15 MINUTES - 100% FREE

---

## 📋 WHAT YOU NEED

- [ ] GitHub account (create at github.com - 2 min)
- [ ] Git installed (download from git-scm.com - 5 min)
- [ ] 15 minutes of time

---

## 🎯 STEP 1: PUSH TO GITHUB (3 minutes)

### 1.1 Create GitHub Repository

1. Go to https://github.com
2. Click "+" → "New repository"
3. Name: `pgt-tms`
4. Visibility: Private
5. Click "Create repository"

### 1.2 Push Your Code

Open PowerShell in your project folder:

```powershell
# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Render deployment"

# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/pgt-tms.git

# Push
git branch -M main
git push -u origin main
```

**✅ Done! Your code is on GitHub**

---

## 🎯 STEP 2: DEPLOY BACKEND (7 minutes)

### 2.1 Sign Up Render

1. Go to https://render.com
2. Click "Get Started"
3. Click "Sign up with GitHub"
4. Authorize Render

**✅ You're logged in!**

### 2.2 Create Backend Service

1. Click "New +" → "Web Service"
2. Click "Connect a repository"
3. Find `pgt-tms` → Click "Connect"

### 2.3 Configure Backend

Fill in:

```
Name: pgt-tms-backend
Region: Oregon (US West)
Branch: main
Root Directory: backend
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
Plan: Free
```

### 2.4 Add Environment Variables

Click "Advanced" → "Add Environment Variable"

Add these (one by one):

```
SECRET_KEY = [Click "Generate" button]
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 1440
ENVIRONMENT = production
```

### 2.5 Add Database

Scroll down → "Add Database"

```
Type: PostgreSQL
Name: pgt-tms-db
Database Name: pgt_tms
Plan: Free
```

### 2.6 Deploy!

1. Click "Create Web Service"
2. Wait 3-5 minutes (watch the logs)
3. When done, you'll see "Live" status

**✅ Backend deployed!**

### 2.7 Initialize Database

1. Click "Shell" tab (top right)
2. Run these commands:

```bash
python init_database.py
python ensure_admin.py
```

**Expected:**
```
✅ Database initialized successfully
✅ Admin user created: admin / admin123
```

### 2.8 Test Backend

Click on your backend URL (top left)

**Expected:** JSON response

**✅ Backend working!**

**Your Backend URL:** `https://pgt-tms-backend.onrender.com`

---

## 🎯 STEP 3: DEPLOY FRONTEND (5 minutes)

### 3.1 Update Frontend Config

In your project, open `frontend/.env.render`

Update with YOUR backend URL:

```env
REACT_APP_API_URL=https://pgt-tms-backend.onrender.com
REACT_APP_ENVIRONMENT=production
REACT_APP_COMPANY_NAME=PGT International (Private) Limited
```

### 3.2 Commit and Push

```powershell
git add frontend/.env.render
git commit -m "Update API URL"
git push
```

### 3.3 Create Frontend Service

1. In Render, click "New +" → "Static Site"
2. Select your `pgt-tms` repository
3. Click "Connect"

### 3.4 Configure Frontend

Fill in:

```
Name: pgt-tms-frontend
Branch: main
Root Directory: frontend
Build Command: npm install && npm run build
Publish Directory: build
Plan: Free
```

### 3.5 Add Environment Variable

Click "Advanced" → "Add Environment Variable"

```
REACT_APP_API_URL = https://pgt-tms-backend.onrender.com
REACT_APP_ENVIRONMENT = production
REACT_APP_COMPANY_NAME = PGT International (Private) Limited
```

**Replace with YOUR actual backend URL!**

### 3.6 Deploy!

1. Click "Create Static Site"
2. Wait 3-5 minutes
3. When done, you'll see "Live" status

**✅ Frontend deployed!**

**Your Frontend URL:** `https://pgt-tms-frontend.onrender.com`

### 3.7 Update CORS

1. Go back to your backend service
2. Click "Environment"
3. Add new variable:

```
ALLOWED_ORIGINS = https://pgt-tms-frontend.onrender.com
```

4. Click "Save Changes"
5. Backend will redeploy (1 minute)

**✅ CORS configured!**

---

## 🎉 DEPLOYMENT COMPLETE!

### Your Live System:

**Frontend (Main App):**
```
https://pgt-tms-frontend.onrender.com
```

**Backend (API):**
```
https://pgt-tms-backend.onrender.com
```

**Login:**
```
Username: admin
Password: admin123
```

---

## 🧪 TEST YOUR DEPLOYMENT

### Test 1: Login

1. Open your frontend URL
2. Enter: `admin` / `admin123`
3. Click "Login"

**Expected:** Dashboard loads ✅

### Test 2: Generate Invoice

1. Click "Receivables" in sidebar
2. Click "Generate Invoice" on any item
3. PDF downloads

**Expected:** Red/Black themed invoice ✅

### Test 3: Generate Statement

1. Click "Staff Payroll" in sidebar
2. Click "Generate Statement" on any staff
3. PDF downloads

**Expected:** Bank statement with running balance ✅

---

## 🎯 DIRECTOR'S AUDIT

### Test 1: Hussain Stress Test
- Navigate to Staff Payroll
- Generate Muhammad Hussain statement
- Verify: PKR 140,000/- balance
- Verify: Running balance column (far right)
- Verify: 28 months remaining

### Test 2: Invoice Generation
- Navigate to Receivables
- Generate invoice
- Verify: Red/Black theme
- Verify: All fields present
- Verify: QR code visible

### Test 3: Pak Afghan Aging
- Navigate to Financial Ledgers
- Generate Pak Afghan report
- Verify: 30+ days highlighted in RED

---

## ✅ SUCCESS CHECKLIST

- [ ] Backend deployed and live
- [ ] Database initialized
- [ ] Admin user created
- [ ] Frontend deployed and live
- [ ] CORS configured
- [ ] Login works
- [ ] Dashboard displays
- [ ] Invoice generates
- [ ] Statement generates
- [ ] All tests pass

---

## 🚨 TROUBLESHOOTING

### Backend deployment fails?

**Check:**
1. Render logs for errors
2. Verify requirements.txt exists
3. Check Python version

**Fix:**
- In Shell: `pip install -r requirements.txt`
- Then: `python init_database.py`

### Frontend shows blank page?

**Check:**
1. Browser console (F12) for errors
2. Verify API URL is correct
3. Check CORS settings

**Fix:**
1. Update ALLOWED_ORIGINS in backend
2. Rebuild frontend with correct API_URL

### Database connection error?

**Check:**
1. DATABASE_URL is set automatically
2. Database is running

**Fix:**
- In Shell: `python init_database.py`

### App spins down?

**This is normal for free tier!**
- Spins down after 15 min inactivity
- Wakes up in 30 seconds
- Perfect for testing

**To keep always on:**
- Upgrade to $7/month plan

---

## 💡 IMPORTANT NOTES

### Free Tier:
- ✅ 100% free
- ✅ HTTPS included
- ✅ PostgreSQL database
- ✅ 750 hours/month
- ⚠️ Spins down after 15 min
- ⚠️ Database expires in 90 days

### Upgrading:
- **Starter:** $7/month (always on)
- **Standard:** $25/month (production)

---

## 📞 NEED HELP?

### Documentation:
- `RENDER_QUICK_START.md` - Quick guide
- `RENDER_DEPLOYMENT_GUIDE.md` - Complete guide
- `README.md` - Project overview

### Render Support:
- https://render.com/docs
- https://render.com/docs/deploy-fastapi

---

## 🎊 CONGRATULATIONS!

**Your PGT International TMS is now LIVE!**

**Share your URL:**
```
https://pgt-tms-frontend.onrender.com
```

**Login and test:**
- Username: admin
- Password: admin123

**Run all 3 Director's audit tests!**

---

## 📝 WHAT'S NEXT?

### After Successful Deployment:

1. **Test thoroughly** - All features
2. **Share URL** - With Director
3. **Run audit tests** - All 3 tests
4. **Gather feedback** - Note improvements
5. **Plan production** - Consider upgrade

### For Production:

1. **Upgrade plan** - $7/month for always-on
2. **Custom domain** - Add your domain
3. **Backup strategy** - Export data regularly
4. **Monitor usage** - Check logs
5. **Security** - Update passwords

---

## 🚀 DEPLOYMENT TIME

**Total Time:** 15-20 minutes

**Breakdown:**
- GitHub setup: 3 minutes
- Backend deployment: 7 minutes
- Frontend deployment: 5 minutes
- Testing: 3 minutes

**Cost:** $0 (FREE!)

---

## 🎉 YOU DID IT!

**Status:** DEPLOYED ✅  
**Platform:** Render.com  
**Cost:** FREE  
**URL:** Live and working  

**Enjoy your free deployment!** 🎊

---

**SHARE YOUR SUCCESS!** 📢

Tell your Director:
"The system is now live at [YOUR_URL]"

**Login credentials:**
- Username: admin
- Password: admin123

**Ready for audit testing!** ✅

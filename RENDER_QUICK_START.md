# ⚡ RENDER.COM - QUICK START

## 🚀 DEPLOY IN 15 MINUTES (FREE)

**Result:** Live system at `https://pgt-tms-frontend.onrender.com`  
**Cost:** $0 (100% FREE)  

---

## 📋 CHECKLIST

### Before You Start:
- [ ] GitHub account
- [ ] Git installed
- [ ] 15 minutes

---

## 🎯 DEPLOYMENT STEPS

### 1️⃣ PUSH TO GITHUB (3 min)

```powershell
# In your project folder
git init
git add .
git commit -m "Ready for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/pgt-tms.git
git branch -M main
git push -u origin main
```

---

### 2️⃣ SIGN UP RENDER.COM (1 min)

1. Go to https://render.com
2. Click "Sign up with GitHub"
3. Authorize Render

---

### 3️⃣ DEPLOY BACKEND (5 min)

1. Click "New +" → "Web Service"
2. Select your `pgt-tms` repository
3. Configure:
   - Name: `pgt-tms-backend`
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Plan: Free

4. Add Environment Variables:
   ```
   SECRET_KEY = [Generate]
   ALGORITHM = HS256
   ACCESS_TOKEN_EXPIRE_MINUTES = 1440
   ```

5. Add Database:
   - Click "New Database"
   - PostgreSQL, Free plan
   - Name: `pgt-tms-db`

6. Click "Create Web Service"

7. Wait 3-5 minutes for deployment

8. Open Shell and run:
   ```bash
   python init_database.py
   python ensure_admin.py
   ```

**Backend URL:** `https://pgt-tms-backend.onrender.com`

---

### 4️⃣ DEPLOY FRONTEND (5 min)

1. Update `frontend/.env.render`:
   ```env
   REACT_APP_API_URL=https://pgt-tms-backend.onrender.com
   ```

2. Commit and push:
   ```powershell
   git add frontend/.env.render
   git commit -m "Update API URL"
   git push
   ```

3. In Render, click "New +" → "Static Site"
4. Select your repository
5. Configure:
   - Name: `pgt-tms-frontend`
   - Root Directory: `frontend`
   - Build: `npm install && npm run build`
   - Publish: `build`
   - Plan: Free

6. Add Environment Variable:
   ```
   REACT_APP_API_URL = https://pgt-tms-backend.onrender.com
   ```

7. Click "Create Static Site"

8. Wait 3-5 minutes

**Frontend URL:** `https://pgt-tms-frontend.onrender.com`

---

### 5️⃣ UPDATE CORS (1 min)

1. Go to backend service
2. Environment → Add:
   ```
   ALLOWED_ORIGINS = https://pgt-tms-frontend.onrender.com
   ```
3. Save (auto-redeploys)

---

### 6️⃣ TEST (2 min)

1. Open: `https://pgt-tms-frontend.onrender.com`
2. Login: `admin` / `admin123`
3. Test: Generate invoice
4. Test: Generate statement

---

## ✅ DONE!

**Your app is LIVE at:**
```
https://pgt-tms-frontend.onrender.com
```

**Login:**
- Username: `admin`
- Password: `admin123`

---

## 🚨 TROUBLESHOOTING

**Backend fails?**
- Check Render logs
- Verify requirements.txt

**Frontend blank?**
- Check API URL in environment
- Check browser console (F12)

**Database error?**
- Verify DATABASE_URL is set
- Run init_database.py in Shell

---

## 💡 IMPORTANT

**Free Tier:**
- Spins down after 15 min inactivity
- Wakes up in 30 seconds
- Perfect for testing!

**To Keep Always On:**
- Upgrade to $7/month Starter plan

---

## 📚 FULL GUIDE

For detailed instructions, see:
`RENDER_DEPLOYMENT_GUIDE.md`

---

**ENJOY YOUR FREE DEPLOYMENT!** 🎉

# Complete ngrok Setup Guide - Step by Step

## ✅ Prerequisites Check

Before starting, make sure:
- [x] Backend is running on http://localhost:8000
- [x] Frontend is running on http://localhost:3000
- [x] Both are working locally

---

## 📥 Step 1: Download and Install ngrok

### Option A: Direct Download (Recommended)
1. Go to: https://ngrok.com/download
2. Click "Download for Windows (64-bit)"
3. Save the ZIP file
4. Extract `ngrok.exe` to `C:\ngrok\` (create this folder if it doesn't exist)

### Option B: Using Chocolatey
```powershell
choco install ngrok
```

---

## 🔑 Step 2: Create Free Account and Get Auth Token

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up (use email or Google/GitHub)
3. After login, go to: https://dashboard.ngrok.com/get-started/your-authtoken
4. Copy your authtoken (looks like: `2abc123def456...`)

---

## ⚙️ Step 3: Configure ngrok

Open PowerShell and run:

```powershell
cd C:\ngrok
.\ngrok config add-authtoken YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with the token you copied.

You should see: `Authtoken saved to configuration file`

---

## 🚀 Step 4: Start ngrok Tunnels

You need to open **TWO** PowerShell windows:

### PowerShell Window 1 - Frontend Tunnel
```powershell
cd C:\ngrok
.\ngrok http 3000 --log=stdout
```

### PowerShell Window 2 - Backend Tunnel
```powershell
cd C:\ngrok
.\ngrok http 8000 --log=stdout
```

**IMPORTANT**: Keep both windows open! Don't close them.

---

## 📋 Step 5: Copy the URLs

Each window will show output like this:

```
Session Status                online
Account                       Your Name (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:3000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy these URLs:**

From Window 1 (Frontend):
```
Frontend URL: https://______.ngrok-free.app
```

From Window 2 (Backend):
```
Backend URL: https://______.ngrok-free.app
```

---

## 🔧 Step 6: Update Frontend Configuration

Now run this PowerShell script with your backend URL:

```powershell
.\UPDATE-BACKEND-URL.ps1 -BackendUrl "https://YOUR-BACKEND-URL.ngrok-free.app"
```

Example:
```powershell
.\UPDATE-BACKEND-URL.ps1 -BackendUrl "https://abc123.ngrok-free.app"
```

---

## 🔄 Step 7: Restart Frontend

1. Go to the terminal where frontend is running
2. Press `Ctrl+C` to stop it
3. Run `npm start` again
4. Wait for "Compiled successfully!" message

---

## 🎉 Step 8: Share with Your Team

Share the **Frontend URL** with your team:

```
https://YOUR-FRONTEND-URL.ngrok-free.app
```

They can access it from:
- ✅ Desktop computers
- ✅ Laptops
- ✅ Tablets
- ✅ Mobile phones
- ✅ Anywhere in the world!

---

## 📱 Mobile Responsive Features

The app is fully responsive and works on:
- 📱 Mobile phones (320px and up)
- 📱 Tablets (768px and up)
- 💻 Laptops (1024px and up)
- 🖥️ Desktop (1280px and up)

Features:
- ✅ Responsive navigation (hamburger menu on mobile)
- ✅ Touch-friendly buttons and inputs
- ✅ Scrollable tables on small screens
- ✅ Adaptive layouts for all screen sizes
- ✅ Optimized forms for mobile entry

---

## 🔍 Testing the Setup

### Test 1: Check Backend Connection
Open in browser: `https://YOUR-BACKEND-URL.ngrok-free.app/docs`

You should see the FastAPI documentation page.

### Test 2: Check Frontend
Open in browser: `https://YOUR-FRONTEND-URL.ngrok-free.app`

You should see the login page.

### Test 3: Login
Use your admin credentials to login and verify everything works.

---

## ⚠️ Important Notes

### Free Plan Limitations:
- ✅ URLs change every time you restart ngrok
- ✅ 2-hour session timeout (need to restart)
- ✅ Limited to 40 connections/minute
- ✅ Perfect for demos and testing!

### Security:
- ✅ HTTPS is automatically enabled
- ✅ ngrok provides secure tunnels
- ✅ Use strong passwords for all accounts
- ✅ Don't share sensitive data during demos

### Performance:
- ⚡ Slight latency due to tunneling
- ⚡ Good enough for demos
- ⚡ For production, use proper hosting

---

## 🛠️ Troubleshooting

### "ngrok: command not found"
- Make sure `ngrok.exe` is in `C:\ngrok\`
- Run commands from `C:\ngrok\` directory

### "Invalid authtoken"
- Double-check you copied the complete token
- No extra spaces before/after
- Run the config command again

### "Tunnel not found" or "Connection refused"
- Make sure backend is running on port 8000
- Make sure frontend is running on port 3000
- Check with: http://localhost:3000 and http://localhost:8000

### "Failed to complete tunnel connection"
- Check your internet connection
- Try restarting ngrok
- Check if firewall is blocking ngrok

### Frontend can't connect to backend
- Make sure you updated the .env file with correct backend URL
- Make sure you restarted the frontend after updating
- Check browser console for errors (F12)

### ngrok "Visit Site" button required
- Free plan shows a warning page first
- Click "Visit Site" button to continue
- This is normal for free ngrok accounts

---

## 📞 Need Help?

If you encounter any issues:

1. Check both ngrok windows are still running
2. Check backend and frontend are still running
3. Verify the backend URL in `frontend/.env` is correct
4. Try restarting everything in this order:
   - Stop ngrok (both windows)
   - Stop frontend (Ctrl+C)
   - Stop backend (Ctrl+C)
   - Start backend
   - Start frontend
   - Start ngrok (both tunnels)
   - Update .env with new backend URL
   - Restart frontend

---

## 🎯 Quick Reference

### Start Everything:
```powershell
# Terminal 1: Backend
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm start

# Terminal 3: ngrok Frontend
cd C:\ngrok
.\ngrok http 3000

# Terminal 4: ngrok Backend
cd C:\ngrok
.\ngrok http 8000

# Terminal 5: Update config
.\UPDATE-BACKEND-URL.ps1 -BackendUrl "https://YOUR-BACKEND.ngrok-free.app"

# Then restart frontend (Terminal 2)
```

### Share with Team:
```
Frontend URL: https://YOUR-FRONTEND.ngrok-free.app
Login: admin / your-password
```

---

## ✅ Success Checklist

- [ ] ngrok installed in C:\ngrok\
- [ ] Auth token configured
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] ngrok frontend tunnel running
- [ ] ngrok backend tunnel running
- [ ] .env file updated with backend URL
- [ ] Frontend restarted after .env update
- [ ] Can access frontend via ngrok URL
- [ ] Can login successfully
- [ ] Tested on mobile device
- [ ] Shared URL with team

---

**Ready to start? Follow the steps above and let me know if you need any help!**

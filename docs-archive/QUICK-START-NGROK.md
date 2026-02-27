# 🚀 Quick Start - ngrok Setup (5 Minutes)

## What You Need

1. Download ngrok: https://ngrok.com/download
2. Extract to `C:\ngrok\`
3. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken

---

## Quick Setup Commands

### 1. Configure ngrok (One Time Only)
```powershell
cd C:\ngrok
.\ngrok config add-authtoken YOUR_TOKEN_HERE
```

### 2. Start Backend Tunnel (Keep Running)
```powershell
cd C:\ngrok
.\ngrok http 8000
```

**Copy the Backend URL** (looks like: `https://abc123.ngrok-free.app`)

### 3. Start Frontend Tunnel (New Window, Keep Running)
```powershell
cd C:\ngrok
.\ngrok http 3000
```

**Copy the Frontend URL** (looks like: `https://xyz789.ngrok-free.app`)

### 4. Update Frontend Config
```powershell
cd C:\Users\PITB\Downloads\pgt-tms
.\UPDATE-BACKEND-URL.ps1 -BackendUrl "https://YOUR-BACKEND-URL.ngrok-free.app"
```

### 5. Restart Frontend
Go to frontend terminal, press `Ctrl+C`, then:
```powershell
npm start
```

### 6. Share Frontend URL with Team
```
https://YOUR-FRONTEND-URL.ngrok-free.app
```

---

## ✅ App is Fully Responsive!

Your team can access from:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets (iPad, Android tablets)
- 💻 Laptops (Windows/Mac/Linux)
- 🖥️ Desktop computers

The app automatically adapts to screen size!

---

## 🎯 What's Next?

1. Follow the steps above
2. When you have the backend URL, tell me: "Backend URL is https://..."
3. I'll verify everything is configured correctly
4. Share the frontend URL with your team
5. Done!

---

## 📞 Need Help?

Just tell me:
- "I'm stuck at step X"
- "I got error: [error message]"
- "ngrok is running, backend URL is https://..."

I'll help you complete the setup!

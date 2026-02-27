# ngrok Setup Instructions - Step by Step

## Step 1: Download ngrok

1. Open this link in your browser: https://ngrok.com/download
2. Click "Download for Windows (64-bit)"
3. Save the ZIP file to your Downloads folder
4. Extract the ZIP file to `C:\ngrok\` (create this folder)

## Step 2: Create Free Account

1. Go to: https://dashboard.ngrok.com/signup
2. Sign up with your email (or use Google/GitHub)
3. After signup, you'll see your dashboard

## Step 3: Get Your Auth Token

1. On the dashboard, click "Your Authtoken" or go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy the token (looks like: 2abc123def456ghi789jkl...)
3. Keep this token ready

## Step 4: Configure ngrok

Open PowerShell and run:

```powershell
cd C:\ngrok
.\ngrok config add-authtoken YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with the token you copied.

## Step 5: Start ngrok Tunnels

You need TWO PowerShell windows:

### PowerShell Window 1 (Frontend):
```powershell
cd C:\ngrok
.\ngrok http 3000 --log=stdout
```

### PowerShell Window 2 (Backend):
```powershell
cd C:\ngrok
.\ngrok http 8000 --log=stdout
```

## Step 6: Copy the URLs

Each window will show something like:

```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:3000
```

**IMPORTANT**: Copy BOTH URLs:
- Frontend URL (from Window 1): `https://______.ngrok-free.app`
- Backend URL (from Window 2): `https://______.ngrok-free.app`

## Step 7: Tell Me the Backend URL

Once you have the backend URL, paste it here in chat, and I'll update the frontend configuration to use it.

Example: "The backend URL is https://xyz789.ngrok-free.app"

---

## Quick Commands Summary

```powershell
# 1. Configure ngrok (one time only)
cd C:\ngrok
.\ngrok config add-authtoken YOUR_TOKEN

# 2. Start frontend tunnel (keep running)
.\ngrok http 3000

# 3. Start backend tunnel (in another window, keep running)
.\ngrok http 8000
```

---

## Troubleshooting

**"ngrok: command not found"**
- Make sure you extracted ngrok.exe to C:\ngrok\
- Run commands from C:\ngrok\ folder

**"Invalid authtoken"**
- Double-check you copied the full token
- Make sure there are no extra spaces

**"Tunnel not found"**
- Make sure your backend (port 8000) and frontend (port 3000) are running
- Check with: http://localhost:3000 and http://localhost:8000

---

## Ready?

Follow the steps above, then tell me:
1. ✅ "ngrok is running"
2. 📋 The backend ngrok URL

I'll then update the frontend and make it fully responsive!

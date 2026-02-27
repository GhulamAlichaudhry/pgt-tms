# Quick Demo Setup - Choose Your Method

## Your Network Information
- IP Address 1: `192.168.16.1`
- IP Address 2: `192.168.5.1`
- IP Address 3: `192.168.100.5`

---

## METHOD 1: Local Network Access (FASTEST - If Team is Nearby)

### Step 1: Configure Windows Firewall
Run these commands in PowerShell as Administrator:

```powershell
# Allow Frontend (Port 3000)
New-NetFirewallRule -DisplayName "PGT TMS Frontend" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow

# Allow Backend (Port 8000)
New-NetFirewallRule -DisplayName "PGT TMS Backend" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

### Step 2: Find Your Active Network IP
Determine which IP your team should use:
- If team is on same WiFi/LAN: Use `192.168.100.5` (most likely)
- Test by pinging from team member's computer

### Step 3: Share These URLs with Your Team
```
Frontend: http://192.168.100.5:3000
Backend:  http://192.168.100.5:8000
```

### Step 4: Update Frontend API Configuration
The frontend needs to know the backend URL. We need to update the axios base URL.

**Pros**: 
- ✅ Works immediately
- ✅ No additional software
- ✅ Fast and stable

**Cons**: 
- ❌ Only works if team is on same network
- ❌ Won't work for remote team

---

## METHOD 2: ngrok (BEST for Remote Team)

### Step 1: Download and Install ngrok
1. Go to: https://ngrok.com/download
2. Download Windows version
3. Extract to a folder (e.g., `C:\ngrok\`)
4. Add to PATH or run from that folder

### Step 2: Sign Up (Free)
1. Create account at: https://dashboard.ngrok.com/signup
2. Get your auth token from: https://dashboard.ngrok.com/get-started/your-authtoken
3. Run: `ngrok config add-authtoken YOUR_TOKEN_HERE`

### Step 3: Start ngrok Tunnels
Open TWO new PowerShell/CMD windows:

**Window 1 - Frontend Tunnel:**
```bash
ngrok http 3000
```

**Window 2 - Backend Tunnel:**
```bash
ngrok http 8000
```

### Step 4: Copy the URLs
ngrok will show something like:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:3000
```

Copy both URLs (frontend and backend).

### Step 5: Update Frontend Configuration
We need to update the frontend to use the ngrok backend URL.

**Pros**: 
- ✅ Works from anywhere in the world
- ✅ HTTPS included
- ✅ No firewall configuration

**Cons**: 
- ❌ Requires ngrok installation
- ❌ URLs change each restart (free plan)
- ❌ Need to update frontend config

---

## METHOD 3: Quick Cloud Deployment (For Professional Demo)

If you want a permanent URL for demos, I can help deploy to:
- **Render.com** (Free, takes 20 minutes)
- **Railway.app** (Free, takes 15 minutes)

---

## WHICH METHOD DO YOU PREFER?

**For team in same office/building**: Use METHOD 1 (Local Network)
**For remote team anywhere**: Use METHOD 2 (ngrok)
**For permanent demo site**: Use METHOD 3 (Cloud)

Let me know which method you'd like, and I'll help you complete the setup!

# 🚀 Quick Start - Remote Demo Setup

## Choose Your Method

### ✅ OPTION A: Team on Same Network (Office/Building)
**Time: 2 minutes | Best for: Local team**

1. **Run Firewall Setup** (Right-click PowerShell → Run as Administrator):
   ```powershell
   cd C:\Users\PITB\Downloads\pgt-tms
   .\setup-firewall.ps1
   ```

2. **Copy the URLs** shown at the end of the script

3. **Share URLs** with your team via WhatsApp/Email

4. **Done!** Team can access immediately

---

### 🌐 OPTION B: Remote Team (Anywhere in World)
**Time: 10 minutes | Best for: Remote team**

#### Step 1: Install ngrok
1. Download: https://ngrok.com/download (Windows 64-bit)
2. Extract to `C:\ngrok\`
3. Open PowerShell in that folder

#### Step 2: Setup ngrok Account
1. Sign up: https://dashboard.ngrok.com/signup
2. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken
3. Run in PowerShell:
   ```bash
   .\ngrok config add-authtoken YOUR_TOKEN_HERE
   ```

#### Step 3: Start Tunnels
Open TWO PowerShell windows:

**Window 1:**
```bash
cd C:\ngrok
.\ngrok http 3000
```

**Window 2:**
```bash
cd C:\ngrok
.\ngrok http 8000
```

#### Step 4: Copy URLs
Each window will show a URL like:
```
Forwarding: https://abc123.ngrok-free.app -> http://localhost:3000
```

Copy BOTH URLs (one from each window).

#### Step 5: Update Frontend
I'll help you update the frontend to use the ngrok backend URL.
Tell me the backend ngrok URL and I'll update the code.

#### Step 6: Share Frontend URL
Share the frontend ngrok URL with your team!

---

## Current Status

✅ Backend running on: http://localhost:8000
✅ Frontend running on: http://localhost:3000

Your IP Addresses:
- 192.168.16.1
- 192.168.5.1
- 192.168.100.5

---

## Which Option Do You Want?

**Reply with:**
- **"A"** for Local Network (same office)
- **"B"** for Remote Access (ngrok)

I'll guide you through the rest!

---

## Troubleshooting

### If Local Network doesn't work:
1. Check both servers are running
2. Try different IP address (192.168.100.5 most likely)
3. Make sure team is on same WiFi
4. Disable VPN if active

### If ngrok doesn't work:
1. Make sure both tunnels are running
2. Check ngrok auth token is configured
3. Frontend needs backend URL update (I'll help)

---

## Need Help?

Just tell me:
1. Which option you want (A or B)
2. Any error messages you see

I'll help you complete the setup!

# Remote Access Setup for Team Demo

## Quick Options for Remote Access

### Option 1: ngrok (RECOMMENDED - Fastest for Demo)
**Best for**: Quick demos, temporary access, no configuration needed

#### Step 1: Install ngrok
1. Download from: https://ngrok.com/download
2. Or install via command:
   ```bash
   # Using Chocolatey (Windows)
   choco install ngrok
   
   # Or download and extract manually
   ```

#### Step 2: Setup ngrok Account (Free)
1. Sign up at https://ngrok.com
2. Get your auth token from dashboard
3. Run: `ngrok config add-authtoken YOUR_AUTH_TOKEN`

#### Step 3: Expose Your Application
```bash
# Terminal 1: Start backend (already running on port 8000)
# Terminal 2: Start frontend (already running on port 3000)

# Terminal 3: Expose frontend
ngrok http 3000

# Terminal 4: Expose backend
ngrok http 8000
```

#### Step 4: Share URLs
- ngrok will give you URLs like:
  - Frontend: `https://abc123.ngrok.io` (share this with team)
  - Backend: `https://xyz789.ngrok.io`

#### Step 5: Update Frontend to Use ngrok Backend
You'll need to update the API URL in your frontend to use the ngrok backend URL.

**Pros**: 
- ✅ Very fast setup (5 minutes)
- ✅ HTTPS included
- ✅ No firewall/router configuration
- ✅ Works from anywhere

**Cons**: 
- ❌ URLs change each time (free plan)
- ❌ Session timeout after 2 hours (free plan)
- ❌ Need to update backend URL in frontend

---

### Option 2: Local Network Access (If Team is on Same Network)
**Best for**: Office/same building, no internet dependency

#### Step 1: Find Your Local IP
```bash
ipconfig
# Look for "IPv4 Address" under your active network adapter
# Example: 192.168.1.100
```

#### Step 2: Update Backend to Allow Network Access
Backend is already configured with `--host 0.0.0.0` ✅

#### Step 3: Configure Windows Firewall
```bash
# Allow port 3000 (Frontend)
netsh advfirewall firewall add rule name="React Dev Server" dir=in action=allow protocol=TCP localport=3000

# Allow port 8000 (Backend)
netsh advfirewall firewall add rule name="FastAPI Backend" dir=in action=allow protocol=TCP localport=8000
```

#### Step 4: Share Your IP with Team
- Frontend: `http://YOUR_IP:3000` (e.g., http://192.168.1.100:3000)
- Backend: `http://YOUR_IP:8000`

**Pros**: 
- ✅ Fast and stable
- ✅ No third-party service
- ✅ No internet required

**Cons**: 
- ❌ Only works on same network
- ❌ Need to configure firewall
- ❌ Team must be physically nearby

---

### Option 3: Tailscale (Best for Secure Remote Access)
**Best for**: Secure, persistent remote access

#### Step 1: Install Tailscale
1. Download from: https://tailscale.com/download
2. Install on your computer
3. Install on team members' computers

#### Step 2: Setup
1. Sign up and login on all devices
2. All devices get added to your private network
3. Each device gets a Tailscale IP (e.g., 100.x.x.x)

#### Step 3: Share Your Tailscale IP
- Find your Tailscale IP in the app
- Share: `http://YOUR_TAILSCALE_IP:3000`

**Pros**: 
- ✅ Secure VPN-like connection
- ✅ Persistent IPs
- ✅ Works from anywhere
- ✅ Free for personal use

**Cons**: 
- ❌ Requires installation on all devices
- ❌ Takes 10-15 minutes to setup

---

### Option 4: Deploy to Cloud (For Production Demo)
**Best for**: Professional demo, persistent access

Quick cloud deployment options:
1. **Render.com** (Free tier available)
2. **Railway.app** (Free tier available)
3. **Heroku** (Paid)
4. **DigitalOcean** (Paid, $5/month)

This requires more setup time (30-60 minutes).

---

## RECOMMENDED APPROACH FOR YOUR DEMO

### Quick Setup with ngrok (5 minutes)

I'll help you set this up right now. Here's what we'll do:

1. Install ngrok
2. Create tunnels for both frontend and backend
3. Update frontend configuration to use ngrok backend URL
4. Share the frontend URL with your team

Would you like me to proceed with ngrok setup?

---

## Alternative: Port Forwarding (If You Have Router Access)

If you have access to your router and a static/dynamic DNS:

1. Forward ports 3000 and 8000 to your computer
2. Use your public IP or setup Dynamic DNS (DynDNS, No-IP)
3. Share: `http://YOUR_PUBLIC_IP:3000`

**Note**: This exposes your computer to the internet - use with caution!

---

## Security Considerations

For any remote access:
1. ✅ Use HTTPS when possible (ngrok provides this)
2. ✅ Use strong passwords for all user accounts
3. ✅ Limit demo duration
4. ✅ Monitor access logs
5. ✅ Disable remote access after demo
6. ⚠️ Don't use production data for demos

---

## Next Steps

Let me know which option you prefer, and I'll help you set it up:

1. **ngrok** - I can guide you through installation and setup
2. **Local Network** - I can help configure firewall rules
3. **Tailscale** - I can provide detailed setup instructions
4. **Cloud Deployment** - I can help deploy to a cloud platform

Which would you like to proceed with?

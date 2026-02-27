# Start Backend Server Manually

## ⚠️ Backend Not Running

The backend server needs to be started for the application to work.

## 🚀 Quick Start

### Option 1: Using Command Prompt (Recommended)

1. Open **Command Prompt** (cmd)
2. Navigate to backend folder:
   ```cmd
   cd C:\Users\PITB\Downloads\pgt-tms\backend
   ```
3. Start the server:
   ```cmd
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
4. Wait for this message:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process
   INFO:     Started server process
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

### Option 2: Using PowerShell

1. Open **PowerShell**
2. Navigate to backend folder:
   ```powershell
   cd C:\Users\PITB\Downloads\pgt-tms\backend
   ```
3. Start the server:
   ```powershell
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## ✅ Verify Backend is Running

Open your browser and go to:
```
http://localhost:8000/docs
```

You should see the **FastAPI** documentation page with all API endpoints.

## 🔐 Now Try Login

Once backend is running:

1. Open: http://localhost:3000
2. Login with:
   - Username: `admin`
   - Password: `admin123`

## 🆘 Troubleshooting

### "Port 8000 is already in use"

Kill existing Python processes:
```cmd
taskkill /F /IM python.exe
taskkill /F /IM python3.12.exe
```

Then start backend again.

### "Module not found" errors

Install requirements:
```cmd
cd backend
pip install -r requirements.txt
```

### "Database error"

Initialize database:
```cmd
cd backend
python init_database.py
python create_admin.py
```

### Backend starts but crashes immediately

Check for errors in the terminal output. Common issues:
- Missing dependencies
- Database file permissions
- Port already in use

## 📝 Keep Backend Running

**IMPORTANT**: Keep the Command Prompt/PowerShell window open!

- Don't close the window where backend is running
- You'll see log messages as you use the app
- Press `Ctrl+C` to stop the backend when done

## 🔄 Restart Backend

If you need to restart:

1. Press `Ctrl+C` in the backend terminal
2. Wait for it to stop
3. Run the start command again:
   ```cmd
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

---

## Quick Summary

```cmd
# 1. Open Command Prompt
# 2. Go to backend folder
cd C:\Users\PITB\Downloads\pgt-tms\backend

# 3. Start backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 4. Verify at http://localhost:8000/docs
# 5. Login at http://localhost:3000 with admin/admin123
```

---

**After starting backend, your login credentials will work!**

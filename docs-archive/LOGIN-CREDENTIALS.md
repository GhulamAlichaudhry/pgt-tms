# Login Credentials - PGT TMS

## ✅ Admin Account Reset Complete

Your admin credentials have been reset and are ready to use:

```
Username: admin
Password: admin123
```

## 🔐 Login Instructions

1. Open the application: http://localhost:3000
2. Enter username: `admin`
3. Enter password: `admin123`
4. Click "Sign In"

## 👥 Default Users

### Administrator
- **Username**: admin
- **Password**: admin123
- **Role**: Administrator
- **Access**: Full system access including:
  - User management
  - All financial reports
  - Profit margins
  - Settings
  - All features

## 🔧 If Login Still Doesn't Work

### Option 1: Reset Password Again
```bash
cd backend
python reset_admin_password.py
# Press Enter or type 'yes' when prompted
```

### Option 2: Create Fresh Admin User
```bash
cd backend
python create_admin.py
```

### Option 3: Check Backend is Running
```bash
# Make sure backend is running on port 8000
# Open browser: http://localhost:8000/docs
# You should see the API documentation
```

### Option 4: Clear Browser Cache
1. Press `Ctrl + Shift + R` to hard refresh
2. Or clear browser cache completely
3. Try logging in again

### Option 5: Check Browser Console
1. Press `F12` to open developer tools
2. Go to "Console" tab
3. Try logging in
4. Look for any error messages
5. Share the error with me if you see one

## 🆘 Troubleshooting

### "Invalid credentials" error
- ✅ Password has been reset to `admin123`
- ✅ Username is `admin` (lowercase)
- ✅ Try clearing browser cache
- ✅ Make sure backend is running

### "Network error" or "Cannot connect"
- ❌ Backend might not be running
- Check: http://localhost:8000/docs
- If not working, start backend:
  ```bash
  cd backend
  python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
  ```

### "User not found"
- Run the reset script again:
  ```bash
  cd backend
  python reset_admin_password.py
  ```

## 📝 After First Login

### Recommended Actions:
1. ✅ Change admin password (Settings → Security)
2. ✅ Create additional users (Settings → User Management)
3. ✅ Set up office expense opening balance
4. ✅ Add your first trip or expense entry

## 🔑 Password Reset Script

If you ever forget the password, just run:

```bash
cd backend
python reset_admin_password.py
```

The script will:
- Reset password to `admin123`
- Ensure user is active
- Show you the credentials

## 📞 Still Having Issues?

Tell me:
1. What error message you see
2. What happens when you try to login
3. Can you access http://localhost:8000/docs?

I'll help you fix it!

---

**Current Status**: ✅ Admin password reset to `admin123`
**Ready to login**: Yes
**Backend running**: Check http://localhost:8000/docs

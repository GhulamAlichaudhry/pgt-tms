# PGT International Transport Management System

## 🚀 Quick Start

### Start the Application
```powershell
# Run this script to start both backend and frontend
.\START-APP.ps1
```

**Access URLs:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8002
- API Docs: http://localhost:8002/docs

**Login Credentials:**
- Admin: `admin` / `admin123`
- Manager: `manager` / `manager123`
- Supervisor: `supervisor` / `supervisor123`

---

## 📋 Features

### Core Functionality
- ✅ Fleet Management & Trip Logging
- ✅ Client & Vendor Management
- ✅ Financial Ledgers (Receivables & Payables)
- ✅ Staff Payroll & Advance Recovery
- ✅ Office Expense Tracking
- ✅ Role-Based Access Control (Admin/Manager/Supervisor)

### Advanced Features
- ✅ **Enhanced PDF Reports** with International Standards
  - Quick Info Box (Outstanding, Last Payment, Status)
  - Monthly Transaction Grouping
  - Color-Coded Payment Status
  - Expense Breakdown & Aging Table
  
- ✅ **Staff Advance Recovery System**
  - Give Advance functionality
  - Automatic monthly deduction
  - Complete ledger with bank statement style
  - Exit alert for pending advances

- ✅ **Receivable Aging Dashboard**
  - 5 aging buckets (Current, 31-60, 61-90, 90+, Total)
  - Color-coded priority system
  - Bulk reminder generation
  - Critical alerts for 90+ days

- ✅ **Supervisor Mobile Form**
  - High-contrast outdoor design
  - Dropdown-only interface
  - Direct camera integration
  - Security: No freight amounts visible

- ✅ **Data Management**
  - Export All Data (Excel with 9 sheets)
  - Export Trip Logs, Staff Records, Financial Ledgers (CSV)
  - Import Data (placeholder)
  - Reset All Data (admin only, with double confirmation)

---

## 🏗️ Project Structure

```
pgt-tms/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main API application
│   ├── models.py           # Database models
│   ├── crud.py             # Database operations
│   ├── auth.py             # Authentication & RBAC
│   ├── schemas.py          # Pydantic schemas
│   ├── enhanced_reports.py # Enhanced PDF generation
│   ├── ledger_service.py   # Financial ledger logic
│   ├── ensure_admin.py     # Auto-reset admin credentials
│   ├── requirements.txt    # Python dependencies
│   └── pgt_tms.db         # SQLite database
│
├── frontend/               # React frontend
│   ├── src/
│   │   ├── pages/         # All page components
│   │   ├── components/    # Reusable components
│   │   ├── contexts/      # React contexts (Auth)
│   │   └── App.js         # Main app component
│   ├── package.json       # Node dependencies
│   └── .env               # Environment variables
│
├── deployment/            # Deployment files
│   ├── QUICK-START.md    # 30-minute deployment guide
│   ├── DEPLOYMENT-STEPS.md
│   ├── DEPLOYMENT-CHECKLIST.md
│   └── (configuration files)
│
├── START-APP.ps1          # Quick start script
├── README.md              # This file
└── DEPLOYMENT.md          # Deployment guide
```

---

## 🔧 Installation

### Prerequisites
- Python 3.9+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python init_database.py
python ensure_admin.py
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm start
```

---

## 📊 Enhanced Reports

### How to Access Enhanced Reports

After logging in, use these direct URLs:

**Pak Afghan Vendor Ledger:**
```
http://localhost:8002/reports/vendor-ledger-pdf-enhanced/1
```

**Financial Summary:**
```
http://localhost:8002/reports/financial-summary-pdf-enhanced
```

**Muhammad Hussain Staff Statement:**
```
http://localhost:8002/reports/staff-statement-pdf-enhanced/3
```

### Verify 4 International Standards:
1. ✅ Quick Info Box (top right)
2. ✅ Monthly Transaction Grouping
3. ✅ Color-Coded Payment Status
4. ✅ Expense Breakdown & Aging Table

---

## 🔐 Role-Based Access Control

### Admin
- Full system access
- View profit margins
- Manage users
- All financial reports
- Export/Import data
- Reset database

### Manager
- Financial reports (NO profit visibility)
- Approve payments
- Staff payroll
- View ledgers
- Expense management

### Supervisor
- Trip entry & management
- Fleet operations
- View trip logs
- Basic reports
- NO financial access
- Mobile form access

---

## 🚀 Deployment

### For cPanel Hosting

See detailed guides:
- **Quick Start:** `deployment/QUICK-START.md` (30 minutes)
- **Detailed Steps:** `deployment/DEPLOYMENT-STEPS.md` (45 minutes)
- **Complete Checklist:** `deployment/DEPLOYMENT-CHECKLIST.md` (60 minutes)

**Target Domain:** tms.pgtinternational.com

**Hosting Details:**
- Server IP: 64.20.56.218
- cPanel: http://64.20.56.218:2082/
- Username: pgtinter

---

## 📱 Mobile Access

Supervisors can access the mobile form at:
```
http://localhost:3000/supervisor-mobile
```

Or on production:
```
https://tms.pgtinternational.com/supervisor-mobile
```

---

## 🔄 Data Management

### Export Data
1. Login as admin
2. Go to Settings → Data Management
3. Click export buttons:
   - Export All Data (Excel)
   - Export Trip Logs (CSV)
   - Export Staff Records (CSV)
   - Export Financial Ledgers (CSV)

### Reset Database (DANGER)
1. Login as admin
2. Go to Settings → Data Management → Danger Zone
3. Click "Reset All Data"
4. Confirm twice (must type "DELETE ALL DATA")
5. All data deleted except user accounts

⚠️ **Always backup before reset!**

---

## 🐛 Troubleshooting

### Login Issues
```bash
cd backend
python reset_admin_password.py
```
Resets admin password to: admin123

### Backend Not Starting
```bash
cd backend
python ensure_admin.py
python main.py
```

### Frontend Not Loading
```bash
cd frontend
npm install
npm start
```

### Database Issues
Delete `backend/pgt_tms.db` and run:
```bash
cd backend
python init_database.py
python add_default_data.py
```

---

## 📞 Support

**Documentation:**
- Main Guide: `DEPLOYMENT.md`
- Settings Guide: `SETTINGS-COMPLETE.md`
- Enhanced Reports: `TEST-ENHANCED-REPORTS-NOW.md`
- Deployment: `START-DEPLOYMENT-HERE.md`

**Logs:**
- Backend: Check terminal running `python main.py`
- Frontend: Check terminal running `npm start`
- Browser: Press F12 → Console tab

---

## 🎯 Key Files

### Essential Backend Files
- `backend/main.py` - Main API with all endpoints
- `backend/models.py` - Database schema
- `backend/enhanced_reports.py` - Enhanced PDF generation
- `backend/ensure_admin.py` - Auto-reset credentials on startup
- `backend/pgt_tms.db` - SQLite database (backup regularly!)

### Essential Frontend Files
- `frontend/src/App.js` - Main app with routing
- `frontend/src/pages/` - All page components
- `frontend/src/contexts/AuthContext.js` - Authentication
- `frontend/.env` - Backend URL configuration

### Essential Scripts
- `START-APP.ps1` - Start both backend and frontend
- `CLEANUP-PROJECT.ps1` - Clean up old documentation files

---

## 📝 Version History

**Version 1.0** (February 2026)
- Complete TMS with accounting integration
- Enhanced PDF reports with international standards
- Staff advance recovery system
- Receivable aging dashboard
- Role-based access control
- Supervisor mobile form
- Data export/import functionality

---

## 🔒 Security Notes

1. **Change Default Passwords** after first login
2. **Backup Database** regularly (use Export All Data)
3. **Use HTTPS** in production (SSL certificate)
4. **Restrict Admin Access** to trusted users only
5. **Never use Reset** in production without backup

---

## 📄 License

Proprietary - PGT International (Private) Limited

---

**Built with:** Python FastAPI + React + SQLite  
**Deployment:** cPanel + Passenger WSGI  
**Status:** ✅ Production Ready  
**Date:** February 2026

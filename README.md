# 🚚 PGT International Transport Management System

A comprehensive transport management system with modern commercial invoicing, staff ledger management, and complete fleet operations tracking.

## 🌟 Features

### Core Modules (16)
- **Dashboard** - Real-time overview and analytics
- **Fleet Logs** - Vehicle and trip management
- **Receivables** - Client billing and payments
- **Payables** - Vendor payments tracking
- **Staff Payroll** - Employee salary and advances
- **Financial Ledgers** - Complete accounting
- **Daily Cash Flow** - Cash register management
- **Expenses** - Office and operational expenses
- **Client Reports** - Custom client statements
- **And more...**

### Modern Invoice System
- ✅ Professional Red/Black theme
- ✅ Commercial invoice format
- ✅ Trip Summary Box (Vehicle, Bilty, Container, Route, Product)
- ✅ Financial table with Halting charges
- ✅ Dual bank details (Meezan & Faysal)
- ✅ QR code verification
- ✅ Terms & Conditions
- ✅ Non-editable PDF security

### Staff Ledger System
- ✅ Bank statement format
- ✅ Running balance column (far right)
- ✅ Color-coded outstanding balances (red)
- ✅ Recovery schedule
- ✅ Professional appearance

## 🚀 Quick Start

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python init_database.py
python ensure_admin.py
uvicorn main:app --reload --port 8002
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Access:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8002
- Login: admin / admin123

## 🌐 Deployment

### Deploy to Render.com (FREE)

**Quick Start:**
See `RENDER_QUICK_START.md` for 15-minute deployment

**Detailed Guide:**
See `RENDER_DEPLOYMENT_GUIDE.md` for complete instructions

**Result:**
- Frontend: `https://pgt-tms-frontend.onrender.com`
- Backend: `https://pgt-tms-backend.onrender.com`
- Cost: $0 (100% FREE)

### Deploy to cPanel

See `DEPLOY_NOW.md` for cPanel deployment instructions

## 📚 Documentation

### Deployment Guides:
- `RENDER_QUICK_START.md` - 15-minute free deployment
- `RENDER_DEPLOYMENT_GUIDE.md` - Complete Render guide
- `DEPLOY_NOW.md` - cPanel deployment
- `STAGING_DEPLOYMENT_GUIDE.md` - Staging server deployment

### System Documentation:
- `FINAL_COMMERCIAL_INVOICE_SYSTEM.md` - Invoice system details
- `SYSTEM_LAUNCHED_SUCCESSFULLY.md` - Launch status
- `DIRECTOR_FINAL_SIGNOFF_PACKAGE.md` - Complete system overview

### Sample Documents:
- `backend/SAMPLE_TRIP_INVOICE.pdf` - Sample commercial invoice
- `backend/SAMPLE_HUSSAIN_STATEMENT.pdf` - Sample staff statement

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL / SQLite
- ReportLab (PDF generation)
- QR Code generation
- JWT Authentication

**Frontend:**
- React
- Tailwind CSS
- Axios
- React Router

## 📦 Project Structure

```
pgt-tms/
├── backend/
│   ├── main.py                          # FastAPI application
│   ├── models.py                        # Database models
│   ├── modern_invoice_generator.py      # Invoice generator
│   ├── staff_ledger_generator.py        # Statement generator
│   └── requirements.txt                 # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js                       # Main React app
│   │   ├── pages/                       # Page components
│   │   └── components/                  # Reusable components
│   └── package.json                     # Node dependencies
├── deployment/                          # Deployment configs
├── RENDER_QUICK_START.md               # Quick deployment guide
└── README.md                           # This file
```

## 🎯 Key Features

### Invoice Generation
- One-click invoice generation from trips
- Professional commercial invoice format
- Automatic calculations (freight + halting)
- QR code for digital verification
- Non-editable PDF security

### Staff Ledger
- Bank statement style format
- Running balance after each transaction
- Color-coded outstanding amounts
- Recovery schedule calculation
- Professional appearance

### Financial Management
- Complete double-entry accounting
- Client and vendor ledgers
- Cash flow tracking
- Expense management
- Comprehensive reporting

## 🔐 Security

- JWT-based authentication
- Password hashing (bcrypt)
- Role-based access control
- Non-editable PDF documents
- Secure API endpoints

## 📊 Database

**Supported:**
- PostgreSQL (Production - Render.com)
- SQLite (Development - Local)
- MySQL (cPanel deployment)

**Auto-migration:**
- Database schema created automatically
- Sample data included
- Admin user auto-created

## 🧪 Testing

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

**Test Features:**
1. Generate invoice from Receivables
2. Generate statement from Staff Payroll
3. View financial ledgers
4. Check daily cash flow

## 📞 Support

**Documentation:**
- See `DEPLOYMENT_INDEX.md` for all guides
- Check `RENDER_DEPLOYMENT_GUIDE.md` for Render help
- Review `STAGING_DEPLOYMENT_GUIDE.md` for cPanel help

**Common Issues:**
- Backend not starting: Check requirements.txt
- Frontend blank: Verify API URL in environment
- Database error: Run init_database.py

## 🎉 Success Criteria

**Deployment successful when:**
- ✅ Frontend loads and login works
- ✅ Dashboard displays all modules
- ✅ Invoices generate with Red/Black theme
- ✅ Statements generate with running balance
- ✅ All calculations accurate

## 📝 License

Proprietary - PGT International (Private) Limited

## 👥 Credits

**Developed for:** PGT International (Private) Limited  
**System:** Transport Management System  
**Version:** 1.0  
**Year:** 2026  

---

## 🚀 Quick Deploy Commands

### Deploy to Render.com:

```bash
# 1. Push to GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/pgt-tms.git
git push -u origin main

# 2. Go to render.com and follow RENDER_QUICK_START.md
```

### Run Locally:

```bash
# Backend
cd backend && pip install -r requirements.txt && python init_database.py && uvicorn main:app --reload --port 8002

# Frontend (new terminal)
cd frontend && npm install && npm start
```

---

**Ready to deploy? Start with `RENDER_QUICK_START.md`!** 🚀

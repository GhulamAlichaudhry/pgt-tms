# PGT International TMS - Live Test Credentials

## 🔐 LOGIN CREDENTIALS

### Admin (Director) Login:
```
URL: http://localhost:3000/login
Username: admin
Password: admin123
Role: ADMIN (Full Access)

Capabilities:
✅ See ALL profit columns
✅ Manage staff advances
✅ View receivable aging
✅ Process payroll
✅ Add/edit trips with freight
✅ Export data
✅ Full dashboard access
```

### Manager Login:
```
URL: http://localhost:3000/login
Username: manager
Password: manager123
Role: MANAGER

Capabilities:
✅ View trips (NO PROFIT COLUMNS)
✅ Manage operations
✅ Process payments
❌ Cannot see profit margins
❌ Cannot see net profit
❌ Cannot delete data
```

### Supervisor Login:
```
URL: http://localhost:3000/login
Username: supervisor
Password: supervisor123
Role: SUPERVISOR

Capabilities:
✅ Mobile form access (/supervisor-mobile)
✅ Enter trip details
✅ Upload Bilty photos
❌ Cannot see freight amounts
❌ Cannot see profit data
❌ Cannot access financial reports
```

---

## 📱 MOBILE FORM ACCESS

### For Port Supervisors (Muhammad Ali, Ammad ud Din):
```
Direct URL: http://localhost:3000/supervisor-mobile

Login as: supervisor / supervisor123
Then navigate to mobile form

Features:
- High-contrast outdoor design
- Large touch targets
- Camera integration
- Dropdown-only interface
- No freight visibility
```

---

## 🧪 LIVE TEST SCENARIO

### Test Case: Sr. No 62 from Log Book

**Trip Details:**
```
Vehicle: JU-9098
Client: Pak Afghan Logistics
Product: [From Log Book]
Route: [From Log Book]
Tonnage: [From Log Book]
Client Freight: 412,000 PKR
Vendor Freight: [From Log Book]
```

### Step-by-Step Test:

#### STEP 1: Supervisor Entry (Mobile)
```
1. Login as: supervisor / supervisor123
2. Navigate to: /supervisor-mobile
3. Fill form:
   - Date: Today
   - Vehicle: Select JU-9098 from dropdown
   - Client: Select "Pak Afghan Logistics"
   - Product: Select from dropdown
   - Destination: Select from dropdown
   - Tonnage: Enter tonnage
   - Bilty Number: Enter "BLT-62"
4. Tap "TAP TO CAPTURE"
5. Take photo (any photo for test)
6. Tap "SUBMIT TRIP"
7. Verify: Success message appears
8. Verify: Form resets

Expected Result:
✅ Trip created with freight = 0
✅ Status = DRAFT
✅ Supervisor never saw freight amounts
```

#### STEP 2: Manager View Test
```
1. Logout supervisor
2. Login as: manager / manager123
3. Navigate to: Fleet Logs
4. Find the trip (BLT-62)
5. Check columns visible

Expected Result:
✅ Can see: Date, Vehicle, Client, Vendor
✅ Can see: Client Freight, Vendor Freight
❌ PROFIT COLUMN DOES NOT EXIST
❌ Cannot calculate margin
✅ Iron Wall verified
```

#### STEP 3: Admin Completion
```
1. Logout manager
2. Login as: admin / admin123
3. Navigate to: Fleet Logs
4. Find trip BLT-62
5. Click Edit/View
6. Add freight amounts:
   - Client Freight: 412,000
   - Vendor Freight: [Amount from log book]
7. Save trip
8. Mark as COMPLETED

Expected Result:
✅ Profit calculated automatically
✅ Receivable created for Pak Afghan
✅ Dashboard updated
```

#### STEP 4: Verify Dashboard Updates
```
1. Go to Dashboard
2. Check Daily Pulse

Expected Result:
✅ Total Revenue increased by 412,000
✅ Profit shows in green
✅ Receivable for Pak Afghan increased
✅ Daily cash flow updated
```

#### STEP 5: Verify Receivable Aging
```
1. Navigate to: /receivable-aging
2. Find Pak Afghan Logistics
3. Check aging buckets

Expected Result:
✅ New 412,000 in "Current (0-30)" bucket
✅ Existing 4.9M in "90+ Days" bucket
✅ Total outstanding updated
✅ Red alert still showing for 90+ days
```

#### STEP 6: Verify Staff Advance (Muhammad Hussain)
```
1. Navigate to: Staff & Payroll
2. Find Muhammad Hussain
3. Check advance balance

Expected Result:
✅ Balance shows 140,000 (or current balance)
✅ Monthly deduction shows 10,000
✅ Yellow warning icon visible
✅ Can view ledger
✅ Can print statement
```

---

## 🔄 DATABASE BACKUP

### Automatic Backup Location:
```
File: backend/pgt_tms.db
Location: backend/ folder
Size: ~5-10 MB

Backup Command:
Copy-Item backend/pgt_tms.db backend/pgt_tms_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db
```

### Manual Backup (Before Live Test):
```powershell
# Run in PowerShell from project root:
cd backend
Copy-Item pgt_tms.db "pgt_tms_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

---

## 📊 EXPORT ALL DATA FEATURE

### New Admin Settings Button:
**Location**: Settings page → Data Management section
**Button**: "Export All Data to Excel"

**Exports Include:**
- All trips with complete details
- All clients and vendors
- All staff and payroll records
- All receivables and payables
- All office expenses
- All staff advance ledger entries
- Financial summary

**File Format**: Excel (.xlsx) with multiple sheets
**Filename**: `PGT_Complete_Data_Export_[Date].xlsx`

---

## ✅ PRE-LIVE TEST CHECKLIST

### Backend Status:
- [x] Database initialized
- [x] All tables created
- [x] Default data loaded
- [x] Admin user created
- [x] Manager user created
- [x] Supervisor user created
- [x] Backup created

### Frontend Status:
- [x] All pages accessible
- [x] Mobile form responsive
- [x] Role-based access working
- [x] Print features functional
- [x] Export features ready

### Security Status:
- [x] Manager Iron Wall active
- [x] Supervisor freight hidden
- [x] Role permissions enforced
- [x] Audit logging enabled

### Integration Status:
- [x] Trip → Receivable (automatic)
- [x] Trip → Payable (automatic)
- [x] Trip → Dashboard (real-time)
- [x] Expense → Dashboard (real-time)
- [x] Payroll → Advance Recovery (automatic)

---

## 🚀 START SERVERS FOR LIVE TEST

### Backend Server:
```powershell
cd backend
python main.py
```
**Expected**: Server running on http://localhost:8002

### Frontend Server:
```powershell
cd frontend
npm start
```
**Expected**: App running on http://localhost:3000

### Verify Both Running:
- Backend: http://localhost:8002/docs (API documentation)
- Frontend: http://localhost:3000 (Login page)

---

## 📞 SUPPORT DURING LIVE TEST

### If Login Fails:
```powershell
cd backend
python reset_admin_password.py
# Password reset to: admin123
```

### If Database Issues:
```powershell
cd backend
# Restore from backup
Copy-Item pgt_tms_backup_[timestamp].db pgt_tms.db
```

### If Frontend Not Loading:
```powershell
cd frontend
npm install
npm start
```

---

## ✅ SUCCESS CRITERIA

### Live Test Passes If:
1. ✅ Supervisor can enter trip without seeing freight
2. ✅ Manager can view trip but NO profit column
3. ✅ Admin can complete trip with freight
4. ✅ Receivable created automatically (412,000)
5. ✅ Dashboard shows updated profit
6. ✅ Aging analysis shows Pak Afghan correctly
7. ✅ Muhammad Hussain's advance balance correct
8. ✅ No errors or crashes

### If All Pass:
**STATUS**: PRODUCTION READY ✅
**NEXT STEP**: Deploy to live server
**TIMELINE**: Tomorrow morning

---

## 🎯 DIRECTOR'S FINAL VERIFICATION

After completing all test steps, verify:

1. **The Brain** (Automatic Calculations):
   - Trip profit calculated correctly
   - Receivable created automatically
   - Dashboard updated in real-time

2. **The Shield** (Security):
   - Manager cannot see profit
   - Supervisor cannot see freight
   - Role-based access enforced

3. **The Mobile Heart** (Port Operations):
   - Mobile form works on phone
   - Camera captures Bilty
   - High-contrast visible in sunlight

4. **The Money Tracker** (Receivables):
   - Pak Afghan 4.9M + 412K visible
   - Aging buckets correct
   - Red alerts showing

5. **The Staff Manager** (Advances):
   - Muhammad Hussain balance correct
   - Auto-recovery working
   - Print statement functional

---

## 🎬 READY FOR LIVE TEST

**Status**: All systems operational
**Credentials**: Provided above
**Backup**: Created and verified
**Support**: Standing by

**Director's Approval**: Awaiting live test results

Once test passes, the business is officially DIGITAL. ✅

# 🧪 TESTING CHECKLIST - ALL FEATURES 1-7

## ✅ QUICK START

### Prerequisites
- [x] Backend running on http://localhost:8002
- [x] Frontend running on http://localhost:3000
- [ ] Email configured in `backend/.env`
- [ ] Admin credentials: admin/admin123

---

## 📋 FEATURE TESTING CHECKLIST

### 1. Database Backup & Restore System

**API Endpoints:**
- [ ] POST /backup/create - Create manual backup
- [ ] GET /backup/list - List all backups
- [ ] POST /backup/restore/{backup_name} - Restore backup
- [ ] DELETE /backup/{backup_name} - Delete backup

**Test Steps:**
```bash
# 1. Get authentication token
curl -X POST http://localhost:8002/token \
  -d "username=admin&password=admin123"

# 2. Create backup
curl -X POST "http://localhost:8002/backup/create?description=Test backup" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. List backups
curl http://localhost:8002/backup/list \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Check backups folder
ls backend/backups/
```

**Expected Results:**
- [ ] Backup created successfully
- [ ] Backup file exists in `backend/backups/`
- [ ] Backup listed in API response
- [ ] Backup has metadata (timestamp, size, description)

---

### 2. Password Reset Functionality

**API Endpoints:**
- [ ] POST /password-reset/request - Request reset
- [ ] POST /password-reset/validate - Validate token
- [ ] POST /password-reset/reset - Reset password

**Frontend Pages:**
- [ ] /forgot-password - Request reset link
- [ ] /reset-password?token=xxx - Reset form

**Test Steps:**
1. [ ] Go to http://localhost:3000/login
2. [ ] Click "Forgot your password?"
3. [ ] Enter email: admin@example.com
4. [ ] Check console/email for reset link
5. [ ] Copy token from link
6. [ ] Open reset link
7. [ ] Enter new password
8. [ ] Login with new password

**Expected Results:**
- [ ] Reset email sent (check console if SMTP not configured)
- [ ] Reset link contains valid token
- [ ] Token validates successfully
- [ ] Password changes successfully
- [ ] Can login with new password
- [ ] Old password no longer works

---

### 3. Invoice Generation System

**API Endpoints:**
- [ ] POST /invoices/generate/{receivable_id} - Generate PDF
- [ ] POST /invoices/email/{receivable_id} - Email invoice

**Test Steps:**
```bash
# 1. Generate invoice PDF
curl -X POST http://localhost:8002/invoices/generate/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output invoice.pdf

# 2. Open invoice.pdf and verify

# 3. Email invoice (if SMTP configured)
curl -X POST http://localhost:8002/invoices/email/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Results:**
- [ ] PDF generated successfully
- [ ] PDF contains company branding
- [ ] Invoice number is correct
- [ ] Client details are correct
- [ ] Amounts are correct
- [ ] PDF is professional and readable
- [ ] Email sent successfully (if configured)

---

### 4. Automated Payment Reminders

**API Endpoints:**
- [ ] POST /reminders/send-all - Send all reminders
- [ ] POST /reminders/send/{receivable_id} - Manual reminder
- [ ] GET /reminders/overdue-summary - Overdue summary
- [ ] GET /reminders/history/{receivable_id} - History

**Test Steps:**
```bash
# 1. Get overdue summary
curl http://localhost:8002/reminders/overdue-summary \
  -H "Authorization: Bearer YOUR_TOKEN"

# 2. Send manual reminder
curl -X POST http://localhost:8002/reminders/send/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Check reminder history
curl http://localhost:8002/reminders/history/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Send all reminders
curl -X POST http://localhost:8002/reminders/send-all \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Results:**
- [ ] Overdue summary shows correct data
- [ ] Manual reminder sent successfully
- [ ] Reminder history tracked
- [ ] All reminders sent successfully
- [ ] Email content is professional
- [ ] Reminder rules applied correctly

---

### 5. Payslip Generation

**API Endpoints:**
- [ ] POST /payslips/generate/{payroll_id} - Generate PDF
- [ ] POST /payslips/email/{payroll_id} - Email payslip
- [ ] POST /payslips/bulk-generate - Bulk generate

**Test Steps:**
```bash
# 1. Generate single payslip
curl -X POST http://localhost:8002/payslips/generate/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output payslip.pdf

# 2. Open payslip.pdf and verify

# 3. Email payslip (if SMTP configured)
curl -X POST http://localhost:8002/payslips/email/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Bulk generate for month
curl -X POST "http://localhost:8002/payslips/bulk-generate?month=2&year=2026" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Results:**
- [ ] PDF generated successfully
- [ ] PDF contains company branding
- [ ] Employee details correct
- [ ] Salary calculations correct
- [ ] Deductions calculated correctly
- [ ] Net payable highlighted
- [ ] Bulk generation works for all staff
- [ ] Email sent successfully (if configured)

---

### 6. Two-Factor Authentication (2FA)

**API Endpoints:**
- [ ] POST /2fa/enable - Enable 2FA
- [ ] POST /2fa/disable - Disable 2FA
- [ ] POST /2fa/send-otp - Send OTP
- [ ] POST /2fa/verify-otp - Verify OTP
- [ ] POST /2fa/generate-backup-codes - Generate codes
- [ ] POST /2fa/verify-backup-code - Verify code
- [ ] GET /2fa/status - Check status

**Test Steps:**
```bash
# 1. Check 2FA status
curl http://localhost:8002/2fa/status \
  -H "Authorization: Bearer YOUR_TOKEN"

# 2. Enable 2FA
curl -X POST http://localhost:8002/2fa/enable \
  -H "Authorization: Bearer YOUR_TOKEN"

# 3. Send OTP
curl -X POST http://localhost:8002/2fa/send-otp \
  -H "Authorization: Bearer YOUR_TOKEN"

# 4. Check email/console for OTP

# 5. Verify OTP (replace 123456 with actual OTP)
curl -X POST "http://localhost:8002/2fa/verify-otp?otp=123456" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 6. Generate backup codes
curl -X POST http://localhost:8002/2fa/generate-backup-codes \
  -H "Authorization: Bearer YOUR_TOKEN"

# 7. Verify backup code
curl -X POST "http://localhost:8002/2fa/verify-backup-code?code=ABC123" \
  -H "Authorization: Bearer YOUR_TOKEN"

# 8. Disable 2FA
curl -X POST http://localhost:8002/2fa/disable \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Results:**
- [ ] 2FA status shows correctly
- [ ] 2FA enables successfully
- [ ] OTP sent to email
- [ ] OTP is 6 digits
- [ ] OTP verifies correctly
- [ ] Invalid OTP rejected
- [ ] OTP expires after 5 minutes
- [ ] Backup codes generated (10 codes)
- [ ] Backup codes work
- [ ] 2FA disables successfully

---

### 7. Bulk Import/Export System

**API Endpoints:**
- [ ] GET /templates/{entity_type} - Download template
- [ ] POST /import/clients - Import clients
- [ ] POST /import/vendors - Import vendors
- [ ] POST /import/staff - Import staff
- [ ] POST /import/vehicles - Import vehicles
- [ ] GET /export/clients - Export clients
- [ ] GET /export/vendors - Export vendors
- [ ] GET /export/staff - Export staff
- [ ] GET /export/trips - Export trips

**Test Steps:**
```bash
# 1. Download client template
curl http://localhost:8002/templates/clients \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output clients_template.xlsx

# 2. Open template and add sample data

# 3. Import clients
curl -X POST http://localhost:8002/import/clients \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@clients_template.xlsx"

# 4. Export clients
curl http://localhost:8002/export/clients \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output clients_export.xlsx

# 5. Export vendors
curl http://localhost:8002/export/vendors \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output vendors_export.xlsx

# 6. Export staff
curl http://localhost:8002/export/staff \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output staff_export.xlsx

# 7. Export trips with date range
curl "http://localhost:8002/export/trips?start_date=2026-01-01&end_date=2026-02-28" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  --output trips_export.xlsx
```

**Expected Results:**
- [ ] Template downloads successfully
- [ ] Template has correct columns
- [ ] Template has sample data/instructions
- [ ] Import validates data
- [ ] Import detects duplicates
- [ ] Import shows success/error count
- [ ] Imported data appears in database
- [ ] Export generates Excel file
- [ ] Export contains all data
- [ ] Export has professional formatting
- [ ] Date range filtering works

---

## 🌐 INTERACTIVE API TESTING

### Using Swagger UI

1. [ ] Open http://localhost:8002/docs
2. [ ] Click "Authorize" button
3. [ ] Enter credentials: admin/admin123
4. [ ] Click "Authorize"
5. [ ] Test each endpoint interactively

**Endpoints to Test:**
- [ ] All backup endpoints
- [ ] All password reset endpoints
- [ ] All invoice endpoints
- [ ] All reminder endpoints
- [ ] All payslip endpoints
- [ ] All 2FA endpoints
- [ ] All import/export endpoints

---

## 📊 VERIFICATION CHECKLIST

### Backend Verification
- [ ] Backend running on port 8002
- [ ] No errors in backend logs
- [ ] All 35+ endpoints visible in /docs
- [ ] Database file exists: backend/pgt_tms.db
- [ ] Backups folder exists: backend/backups/

### Frontend Verification
- [ ] Frontend running on port 3000
- [ ] Login page accessible
- [ ] Forgot password link visible
- [ ] Reset password page accessible
- [ ] No console errors

### Email Configuration
- [ ] SMTP settings in backend/.env
- [ ] Test email sending
- [ ] Verify email templates
- [ ] Check email delivery

### Security Verification
- [ ] Authentication required for all endpoints
- [ ] Admin-only endpoints protected
- [ ] 2FA working correctly
- [ ] Password reset tokens secure
- [ ] Backup system secure

---

## 🎯 SUCCESS CRITERIA

### All Features Working
- [ ] All 7 features tested
- [ ] All API endpoints working
- [ ] No critical errors
- [ ] Professional output (PDFs, emails)
- [ ] Data validation working
- [ ] Error handling working

### Performance
- [ ] Invoice generation < 2 seconds
- [ ] Backup creation < 30 seconds
- [ ] Bulk import < 1 minute for 100 records
- [ ] API response time < 500ms

### User Experience
- [ ] Clear error messages
- [ ] Professional PDFs
- [ ] Professional emails
- [ ] Easy to use API
- [ ] Good documentation

---

## 🐛 TROUBLESHOOTING

### Backend Not Starting
```bash
cd backend
python main.py
# Check for errors in output
```

### Email Not Sending
- Check SMTP settings in backend/.env
- Verify email credentials
- Check email service logs
- Test with Gmail app password

### Import Failing
- Verify Excel file format
- Check column names match template
- Verify data types
- Check for duplicate entries

### PDF Not Generating
- Check ReportLab installation
- Verify file permissions
- Check disk space
- Review backend logs

---

## 📝 NOTES

### Test Data
- Use existing data in database
- Create test receivables for invoices
- Create test payroll for payslips
- Use sample data for imports

### Email Testing
- If SMTP not configured, check console logs
- Email content will be printed to console
- Configure SMTP for production testing

### Backup Testing
- Test with small database first
- Verify backup file integrity
- Test restore on copy of database
- Keep safety backups

---

## ✅ COMPLETION CHECKLIST

- [ ] All 7 features tested
- [ ] All endpoints working
- [ ] Documentation reviewed
- [ ] Email configured
- [ ] Cron jobs set up (optional)
- [ ] Frontend UI planned
- [ ] User training planned
- [ ] Production deployment planned

---

**Testing Date:** _____________
**Tested By:** _____________
**Status:** _____________
**Notes:** _____________

---

**Last Updated:** February 27, 2026
**Status:** Ready for Testing
**All Features:** IMPLEMENTED ✅

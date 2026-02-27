# Quick Integration Reference Card

## 🎯 Core Principle
**Trip is master → All cash through ONE register → Backend calculates everything**

---

## 📊 Cash Register Rules

### Direction:
- **IN** = Money coming in (client payments)
- **OUT** = Money going out (vendor payments, expenses, salaries)

### Source Modules:
- **receivable** = Client payment (IN)
- **payable** = Vendor payment (OUT) - NOT an expense!
- **expense** = Operating expense (OUT) - fuel, office, etc.
- **payroll** = Salary payment (OUT)
- **adjustment** = Admin only

---

## 🔄 Integration Points

| Event | Action | Cash Register |
|-------|--------|---------------|
| Client pays | Update receivable | IN, receivable |
| Vendor paid | Update payable | OUT, payable |
| Add expense | Create expense | OUT, expense |
| Pay salary | Create payroll | OUT, payroll |

---

## 💰 Key Calculations

```
Gross Profit = Client Freight - (Vendor Freight + Local/Shifting)
Net Profit = Gross Profit - Total Expenses
Cash Balance = SUM(IN) - SUM(OUT)
```

---

## 🚀 Deployment (3 Steps)

```bash
# 1. Run migration
python backend/migrate_complete_integration.py

# 2. Update crud.py (4 functions)
# - create_collection → cash_register.record_client_payment()
# - update_payment_request → cash_register.record_vendor_payment()
# - create_expense → cash_register.record_expense_payment()
# - create_payroll_entry → cash_register.record_payroll_payment()

# 3. Restart backend
python backend/main.py
```

---

## ✅ Test Checklist

- [ ] Client payment → Check logs for "Cash Register: IN"
- [ ] Vendor payment → Check logs for "Cash Register: OUT"
- [ ] Expense → Check logs for "Cash Register: OUT"
- [ ] Dashboard → Verify cash balance
- [ ] Query: `SELECT * FROM cash_transactions ORDER BY id DESC LIMIT 10;`

---

## 🔐 Security

- ✅ created_by on all records
- ✅ Soft delete only
- ✅ Admin-only adjustments
- ✅ Audit trail

---

## 📁 Key Files

- `backend/cash_register_service.py` - Central service
- `backend/models.py` - CashTransaction model
- `backend/crud.py` - Update 4 functions
- `backend/migrate_complete_integration.py` - Migration

---

## 🎯 Success Indicators

✅ cash_transactions table exists  
✅ Every payment creates cash record  
✅ Dashboard shows correct balance  
✅ Vendor payments NOT in expenses  
✅ Backend logs show "Cash Register: IN/OUT"  

---

**That's it! Simple, automated, reliable.** 🎉

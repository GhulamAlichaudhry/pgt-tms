# Director's Final 20% - Implementation Plan

## Acknowledged: Director's 3 Mandatory Rules

### Rule 1: "Hussain" Recovery Logic - Smart Ledger ✅
**Requirement**: Complete advance tracking with history
- Original Advance: 140,000
- Current Balance: Auto-calculated
- Next Deduction: Shown in payroll
- Exit Flag: Alert on staff termination

### Rule 2: "Manager" Iron Wall - Security ✅
**Requirement**: Zero profit visibility for Manager role
- Managers see: Freight In, Freight Out ONLY
- Profit column: Hidden completely
- Only Director (Admin) sees green profit numbers

### Rule 3: Supervisor "One-Touch" Form ✅
**Requirement**: Mobile-ready, dropdown-driven
- Dropdowns: Vehicles, Clients, Vendors, Products
- Camera integration: Direct Bilty photo upload
- Required field: Cannot save without photo
- No profit/rate visibility

### Rule 4: Receivable Aging Report ✅
**Requirement**: 30/60/90 days aging analysis
- Show overdue receivables by age bracket
- Client-wise breakdown
- Export to Excel

---

## Implementation Order (Starting Now)

### Phase 1: Staff Advance Recovery (2 hours)
1. Create `staff_advances` table
2. Add recovery fields to `staff` table
3. Modify payroll calculation
4. Build Recovery Ledger UI
5. Add exit flag logic

### Phase 2: Manager Iron Wall (1 hour)
1. Add role-based field visibility
2. Hide profit columns for Manager
3. Test security thoroughly

### Phase 3: Supervisor Mobile Form (2 hours)
1. Create simplified mobile view
2. Add camera/photo upload
3. Implement dropdowns
4. Hide sensitive data

### Phase 4: Receivable Aging Report (2 hours)
1. Create aging calculation logic
2. Build report UI
3. Add Excel export

**Total Time**: 7 hours
**Status**: Starting Phase 1 immediately

---

## Deliverables for Director's Audit
1. Screenshots of Staff Recovery Ledger
2. Video of Manager view (no profit visible)
3. Mobile Supervisor form demo
4. Receivable Aging Report sample

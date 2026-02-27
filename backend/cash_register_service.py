"""
Central Cash Register Service (TASK 1 - MOST IMPORTANT)

CORE PRINCIPLE:
- Trip is the master record
- No manual duplication of financial data
- All cash movement must pass through ONE central cash register
- Dashboard performs no calculations — backend aggregation only

MANDATORY RULES:
- No direct UI entry except admin adjustments
- Every payment event MUST insert a record here
- Vendor payments are NOT expenses (cost already captured at trip creation)
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from datetime import datetime, date
from typing import Optional
import models

class CashRegisterService:
    """Central Cash Register - Single Source of Truth"""
    
    def __init__(self, db: Session):
        self.db = db
    
    # ============================================
    # CORE CASH REGISTER OPERATIONS
    # ============================================
    
    def record_cash_transaction(
        self,
        date: date,
        amount: float,
        direction: models.CashDirection,
        source_module: models.CashSourceModule,
        source_id: int,
        payment_mode: models.PaymentMode,
        created_by: int,
        reference: Optional[str] = None,
        note: Optional[str] = None
    ) -> models.CashTransaction:
        """
        Record a cash transaction in the central register
        
        MANDATORY: Every payment event MUST call this
        """
        transaction = models.CashTransaction(
            date=date,
            amount=amount,
            direction=direction,
            source_module=source_module,
            source_id=source_id,
            payment_mode=payment_mode,
            reference=reference,
            note=note,
            created_by=created_by
        )
        
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        
        print(f"✅ Cash Register: {direction.value} PKR {amount:,.2f} from {source_module.value} #{source_id}")
        
        return transaction
    
    # ============================================
    # TASK 2.1: CLIENT RECEIVABLES INTEGRATION
    # ============================================
    
    def record_client_payment(
        self,
        collection: models.Collection,
        created_by: int
    ) -> models.CashTransaction:
        """
        When a client payment is recorded:
        1. Update receivable balance (done in crud.py)
        2. Insert cash_transactions record: direction = IN, source_module = receivable
        """
        # Convert collection channel to payment mode
        payment_mode_map = {
            models.CollectionChannel.BANK_TRANSFER: models.PaymentMode.BANK,
            models.CollectionChannel.CASH: models.PaymentMode.CASH,
            models.CollectionChannel.CHEQUE: models.PaymentMode.CHEQUE,
            models.CollectionChannel.ONLINE_TRANSFER: models.PaymentMode.ONLINE,
            models.CollectionChannel.MOBILE_BANKING: models.PaymentMode.MOBILE,
            models.CollectionChannel.CREDIT_CARD: models.PaymentMode.ONLINE,
        }
        
        payment_mode = payment_mode_map.get(
            collection.collection_channel,
            models.PaymentMode.BANK
        )
        
        client_name = collection.client.name if collection.client else "Unknown"
        
        return self.record_cash_transaction(
            date=collection.collection_date.date() if isinstance(collection.collection_date, datetime) else collection.collection_date,
            amount=collection.collection_amount,
            direction=models.CashDirection.IN,
            source_module=models.CashSourceModule.RECEIVABLE,
            source_id=collection.id,
            payment_mode=payment_mode,
            created_by=created_by,
            reference=collection.reference_number,
            note=f"Payment from {client_name}: {collection.notes or ''}"
        )
    
    # ============================================
    # TASK 2.2: VENDOR PAYABLES INTEGRATION
    # ============================================
    
    def record_vendor_payment(
        self,
        payment_request: models.PaymentRequest,
        created_by: int
    ) -> models.CashTransaction:
        """
        When a vendor payment is recorded:
        1. Update payable balance (done in crud.py)
        2. Insert cash_transactions record: direction = OUT, source_module = payable
        
        IMPORTANT: Vendor payments must NOT be counted as expenses
        (cost already captured at trip creation)
        """
        # Convert payment channel to payment mode
        payment_mode_map = {
            models.PaymentChannel.BANK_TRANSFER: models.PaymentMode.BANK,
            models.PaymentChannel.CASH: models.PaymentMode.CASH,
            models.PaymentChannel.CHEQUE: models.PaymentMode.CHEQUE,
            models.PaymentChannel.ONLINE_TRANSFER: models.PaymentMode.ONLINE,
            models.PaymentChannel.MOBILE_BANKING: models.PaymentMode.MOBILE,
        }
        
        payment_mode = payment_mode_map.get(
            payment_request.payment_channel,
            models.PaymentMode.BANK
        )
        
        vendor_name = payment_request.vendor.name if payment_request.vendor else "Unknown"
        
        return self.record_cash_transaction(
            date=payment_request.payment_date.date() if isinstance(payment_request.payment_date, datetime) else payment_request.payment_date or date.today(),
            amount=payment_request.requested_amount,
            direction=models.CashDirection.OUT,
            source_module=models.CashSourceModule.PAYABLE,
            source_id=payment_request.id,
            payment_mode=payment_mode,
            created_by=created_by,
            reference=payment_request.payment_reference,
            note=f"Payment to {vendor_name}: {payment_request.payment_notes or ''}"
        )
    
    # ============================================
    # TASK 2.3: EXPENSES INTEGRATION
    # ============================================
    
    def record_expense_payment(
        self,
        expense: models.Expense,
        created_by: int
    ) -> models.CashTransaction:
        """
        When an expense is marked as paid:
        1. Create expense record (done in crud.py)
        2. Insert cash_transactions record: direction = OUT, source_module = expense
        """
        return self.record_cash_transaction(
            date=expense.date.date() if isinstance(expense.date, datetime) else expense.date,
            amount=expense.amount,
            direction=models.CashDirection.OUT,
            source_module=models.CashSourceModule.EXPENSE,
            source_id=expense.id,
            payment_mode=models.PaymentMode.CASH,  # Default for expenses
            created_by=created_by,
            reference=None,
            note=f"Expense: {expense.category} - {expense.description}"
        )
    
    # ============================================
    # TASK 2.4: STAFF PAYROLL INTEGRATION
    # ============================================
    
    def record_payroll_payment(
        self,
        payroll: models.PayrollEntry,
        created_by: int
    ) -> models.CashTransaction:
        """
        When salary is processed:
        1. Create expense record (salary) - done in crud.py
        2. Insert cash_transactions record: direction = OUT, source_module = payroll
        """
        staff_name = payroll.staff.name if payroll.staff else "Unknown"
        
        return self.record_cash_transaction(
            date=date.today(),
            amount=payroll.net_payable,
            direction=models.CashDirection.OUT,
            source_module=models.CashSourceModule.PAYROLL,
            source_id=payroll.id,
            payment_mode=models.PaymentMode.BANK,  # Default for salaries
            created_by=created_by,
            reference=None,
            note=f"Salary for {staff_name} - {payroll.month}/{payroll.year}"
        )
    
    # ============================================
    # ADMIN ADJUSTMENTS (TASK 8)
    # ============================================
    
    def record_adjustment(
        self,
        date: date,
        amount: float,
        direction: models.CashDirection,
        created_by: int,
        reference: Optional[str] = None,
        note: Optional[str] = None
    ) -> models.CashTransaction:
        """
        Admin-only: Record manual adjustment
        Used for opening balances or corrections
        """
        return self.record_cash_transaction(
            date=date,
            amount=amount,
            direction=direction,
            source_module=models.CashSourceModule.ADJUSTMENT,
            source_id=0,  # No source for adjustments
            payment_mode=models.PaymentMode.BANK,
            created_by=created_by,
            reference=reference,
            note=note
        )
    
    # ============================================
    # TASK 5: DASHBOARD BACKEND CALCULATIONS
    # ============================================
    
    def get_cash_balance(self) -> float:
        """
        Calculate current cash balance
        Cash Balance = SUM(IN) - SUM(OUT)
        """
        cash_in = self.db.query(func.sum(models.CashTransaction.amount)).filter(
            models.CashTransaction.direction == models.CashDirection.IN,
            models.CashTransaction.is_deleted == False
        ).scalar() or 0.0
        
        cash_out = self.db.query(func.sum(models.CashTransaction.amount)).filter(
            models.CashTransaction.direction == models.CashDirection.OUT,
            models.CashTransaction.is_deleted == False
        ).scalar() or 0.0
        
        return cash_in - cash_out
    
    def get_today_cash_flow(self) -> dict:
        """
        Get today's cash IN and OUT
        """
        today = date.today()
        
        cash_in = self.db.query(func.sum(models.CashTransaction.amount)).filter(
            models.CashTransaction.date == today,
            models.CashTransaction.direction == models.CashDirection.IN,
            models.CashTransaction.is_deleted == False
        ).scalar() or 0.0
        
        cash_out = self.db.query(func.sum(models.CashTransaction.amount)).filter(
            models.CashTransaction.date == today,
            models.CashTransaction.direction == models.CashDirection.OUT,
            models.CashTransaction.is_deleted == False
        ).scalar() or 0.0
        
        return {
            "cash_in": cash_in,
            "cash_out": cash_out,
            "net": cash_in - cash_out
        }
    
    # ============================================
    # TASK 6: DAILY CASH FLOW
    # ============================================
    
    def get_daily_cash_flow(
        self,
        start_date: date,
        end_date: date
    ) -> list:
        """
        Get daily cash flow for date range
        Returns: opening balance, cash IN, cash OUT, closing balance per day
        """
        # Get opening balance (all transactions before start_date)
        opening_in = self.db.query(func.sum(models.CashTransaction.amount)).filter(
            models.CashTransaction.date < start_date,
            models.CashTransaction.direction == models.CashDirection.IN,
            models.CashTransaction.is_deleted == False
        ).scalar() or 0.0
        
        opening_out = self.db.query(func.sum(models.CashTransaction.amount)).filter(
            models.CashTransaction.date < start_date,
            models.CashTransaction.direction == models.CashDirection.OUT,
            models.CashTransaction.is_deleted == False
        ).scalar() or 0.0
        
        opening_balance = opening_in - opening_out
        
        # Get transactions for date range grouped by date
        from sqlalchemy import case
        
        daily_data = self.db.query(
            models.CashTransaction.date,
            func.sum(case((models.CashTransaction.direction == models.CashDirection.IN, models.CashTransaction.amount), else_=0)).label('cash_in'),
            func.sum(case((models.CashTransaction.direction == models.CashDirection.OUT, models.CashTransaction.amount), else_=0)).label('cash_out')
        ).filter(
            and_(
                models.CashTransaction.date >= start_date,
                models.CashTransaction.date <= end_date,
                models.CashTransaction.is_deleted == False
            )
        ).group_by(models.CashTransaction.date).order_by(models.CashTransaction.date).all()
        
        # Build daily flow with running balance
        result = []
        running_balance = opening_balance
        
        for row in daily_data:
            cash_in = float(row.cash_in)
            cash_out = float(row.cash_out)
            net = cash_in - cash_out
            running_balance += net
            
            result.append({
                "date": row.date.isoformat(),
                "opening_balance": running_balance - net,
                "cash_in": cash_in,
                "cash_out": cash_out,
                "net": net,
                "closing_balance": running_balance
            })
        
        return result
    
    # ============================================
    # SOFT DELETE (TASK 8)
    # ============================================
    
    def soft_delete_transaction(
        self,
        transaction_id: int,
        deleted_by: int
    ) -> bool:
        """
        Soft delete a cash transaction (admin only)
        """
        transaction = self.db.query(models.CashTransaction).filter(
            models.CashTransaction.id == transaction_id
        ).first()
        
        if not transaction:
            return False
        
        transaction.is_deleted = True
        transaction.deleted_by = deleted_by
        transaction.deleted_at = datetime.now()
        
        self.db.commit()
        return True

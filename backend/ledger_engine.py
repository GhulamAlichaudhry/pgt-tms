"""
Ledger Engine - Core accounting engine for PGT TMS
Implements double-entry bookkeeping principles adapted for transport operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_, desc, func
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import logging

from models import LedgerEntry, LedgerType, TransactionType, Client, Vendor, CashBankAccount
from database import SessionLocal

logger = logging.getLogger(__name__)

class TransactionData:
    """Data structure for transaction information"""
    def __init__(self, 
                 ledger_type: LedgerType,
                 entity_id: int,
                 date: datetime,
                 description: str,
                 debit_amount: float = 0.0,
                 credit_amount: float = 0.0,
                 reference_no: str = None,
                 transaction_type: TransactionType = None,
                 created_by: int = None):
        self.ledger_type = ledger_type
        self.entity_id = entity_id
        self.date = date
        self.description = description
        self.debit_amount = debit_amount
        self.credit_amount = credit_amount
        self.reference_no = reference_no
        self.transaction_type = transaction_type
        self.created_by = created_by

class ValidationResult:
    """Result of transaction validation"""
    def __init__(self, is_valid: bool, errors: List[str] = None):
        self.is_valid = is_valid
        self.errors = errors or []

class LedgerEngine:
    """
    Core ledger engine implementing double-entry bookkeeping
    Formula: Opening Balance + Credits - Debits = Running Balance
    """
    
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal()
    
    def create_entry(self, transaction_data: TransactionData) -> LedgerEntry:
        """
        Create a new ledger entry with automatic balance calculation
        
        Args:
            transaction_data: Transaction information
            
        Returns:
            Created LedgerEntry
            
        Raises:
            ValueError: If validation fails
        """
        # Validate transaction
        validation = self.validate_transaction(transaction_data)
        if not validation.is_valid:
            raise ValueError(f"Transaction validation failed: {', '.join(validation.errors)}")
        
        try:
            # Calculate running balance
            current_balance = self.get_running_balance(
                transaction_data.ledger_type, 
                transaction_data.entity_id
            )
            
            # Apply transaction: Balance + Credits - Debits
            new_balance = current_balance + transaction_data.credit_amount - transaction_data.debit_amount
            
            # Create ledger entry
            ledger_entry = LedgerEntry(
                ledger_type=transaction_data.ledger_type,
                entity_id=transaction_data.entity_id,
                date=transaction_data.date,
                description=transaction_data.description,
                debit_amount=transaction_data.debit_amount,
                credit_amount=transaction_data.credit_amount,
                running_balance=new_balance,
                reference_no=transaction_data.reference_no,
                transaction_type=transaction_data.transaction_type,
                created_by=transaction_data.created_by,
                is_immutable=True
            )
            
            self.db.add(ledger_entry)
            self.db.commit()
            self.db.refresh(ledger_entry)
            
            # Update entity balance
            self._update_entity_balance(
                transaction_data.ledger_type,
                transaction_data.entity_id,
                new_balance
            )
            
            logger.info(f"Created ledger entry: {ledger_entry.id} for {transaction_data.ledger_type.value} {transaction_data.entity_id}")
            return ledger_entry
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Failed to create ledger entry: {str(e)}")
            raise
    
    def get_running_balance(self, ledger_type: LedgerType, entity_id: int) -> float:
        """
        Get current running balance for an entity
        
        Args:
            ledger_type: Type of ledger (client, vendor, cash_bank)
            entity_id: ID of the entity
            
        Returns:
            Current running balance
        """
        latest_entry = self.db.query(LedgerEntry).filter(
            and_(
                LedgerEntry.ledger_type == ledger_type,
                LedgerEntry.entity_id == entity_id
            )
        ).order_by(desc(LedgerEntry.date), desc(LedgerEntry.id)).first()
        
        return latest_entry.running_balance if latest_entry else 0.0
    
    def get_ledger_history(self, 
                          ledger_type: LedgerType, 
                          entity_id: int,
                          start_date: date = None,
                          end_date: date = None,
                          limit: int = 100) -> List[LedgerEntry]:
        """
        Get ledger history for an entity with optional date filtering
        
        Args:
            ledger_type: Type of ledger
            entity_id: ID of the entity
            start_date: Optional start date filter
            end_date: Optional end date filter
            limit: Maximum number of entries to return
            
        Returns:
            List of ledger entries
        """
        query = self.db.query(LedgerEntry).filter(
            and_(
                LedgerEntry.ledger_type == ledger_type,
                LedgerEntry.entity_id == entity_id
            )
        )
        
        if start_date:
            query = query.filter(LedgerEntry.date >= start_date)
        if end_date:
            query = query.filter(LedgerEntry.date <= end_date)
        
        return query.order_by(desc(LedgerEntry.date), desc(LedgerEntry.id)).limit(limit).all()
    
    def validate_transaction(self, transaction_data: TransactionData) -> ValidationResult:
        """
        Validate transaction data before creating ledger entry
        
        Args:
            transaction_data: Transaction to validate
            
        Returns:
            ValidationResult with validation status and errors
        """
        errors = []
        
        # Basic validation
        if not transaction_data.entity_id:
            errors.append("Entity ID is required")
        
        if not transaction_data.date:
            errors.append("Transaction date is required")
        
        if not transaction_data.description:
            errors.append("Description is required")
        
        if transaction_data.debit_amount < 0 or transaction_data.credit_amount < 0:
            errors.append("Amounts cannot be negative")
        
        if transaction_data.debit_amount == 0 and transaction_data.credit_amount == 0:
            errors.append("Either debit or credit amount must be greater than zero")
        
        if transaction_data.debit_amount > 0 and transaction_data.credit_amount > 0:
            errors.append("Cannot have both debit and credit amounts in single entry")
        
        # Entity existence validation
        if transaction_data.ledger_type == LedgerType.CLIENT:
            client = self.db.query(Client).filter(Client.id == transaction_data.entity_id).first()
            if not client:
                errors.append(f"Client with ID {transaction_data.entity_id} not found")
            elif not client.is_active:
                errors.append(f"Client {client.name} is not active")
        
        elif transaction_data.ledger_type == LedgerType.VENDOR:
            vendor = self.db.query(Vendor).filter(Vendor.id == transaction_data.entity_id).first()
            if not vendor:
                errors.append(f"Vendor with ID {transaction_data.entity_id} not found")
            elif not vendor.is_active:
                errors.append(f"Vendor {vendor.name} is not active")
        
        elif transaction_data.ledger_type == LedgerType.CASH_BANK:
            account = self.db.query(CashBankAccount).filter(CashBankAccount.id == transaction_data.entity_id).first()
            if not account:
                errors.append(f"Cash/Bank account with ID {transaction_data.entity_id} not found")
            elif not account.is_active:
                errors.append(f"Account {account.account_name} is not active")
        
        # Date validation (prevent backdating beyond configured limit) - Skip for migration
        # if transaction_data.date.date() < (datetime.now().date().replace(day=1)):  # No backdating beyond current month
        #     errors.append("Cannot backdate transactions beyond current month")
        
        return ValidationResult(len(errors) == 0, errors)
    
    def _update_entity_balance(self, ledger_type: LedgerType, entity_id: int, new_balance: float):
        """
        Update the cached balance in the entity table
        
        Args:
            ledger_type: Type of ledger
            entity_id: ID of the entity
            new_balance: New balance to set
        """
        try:
            if ledger_type == LedgerType.CLIENT:
                client = self.db.query(Client).filter(Client.id == entity_id).first()
                if client:
                    client.current_balance = new_balance
            
            elif ledger_type == LedgerType.VENDOR:
                vendor = self.db.query(Vendor).filter(Vendor.id == entity_id).first()
                if vendor:
                    vendor.current_balance = new_balance
            
            elif ledger_type == LedgerType.CASH_BANK:
                account = self.db.query(CashBankAccount).filter(CashBankAccount.id == entity_id).first()
                if account:
                    account.current_balance = new_balance
            
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Failed to update entity balance: {str(e)}")
            self.db.rollback()
    
    def get_total_receivables(self) -> float:
        """
        Calculate total receivables (sum of positive client balances)
        
        Returns:
            Total amount receivable from clients
        """
        result = self.db.query(func.sum(Client.current_balance)).filter(
            and_(Client.current_balance > 0, Client.is_active == True)
        ).scalar()
        
        return result or 0.0
    
    def get_total_payables(self) -> float:
        """
        Calculate total payables (sum of positive vendor balances)
        
        Returns:
            Total amount payable to vendors
        """
        result = self.db.query(func.sum(Vendor.current_balance)).filter(
            and_(Vendor.current_balance > 0, Vendor.is_active == True)
        ).scalar()
        
        return result or 0.0
    
    def get_cash_bank_balance(self) -> float:
        """
        Calculate total cash and bank balance
        
        Returns:
            Total cash and bank balance
        """
        result = self.db.query(func.sum(CashBankAccount.current_balance)).filter(
            CashBankAccount.is_active == True
        ).scalar()
        
        return result or 0.0
    
    def get_daily_cash_flow(self, target_date: date) -> Dict[str, float]:
        """
        Calculate daily cash flow for a specific date
        
        Args:
            target_date: Date to calculate cash flow for
            
        Returns:
            Dictionary with daily_income, daily_outgoing, daily_net
        """
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = datetime.combine(target_date, datetime.max.time())
        
        # Daily income (payments received - debits to client ledgers)
        daily_income = self.db.query(func.sum(LedgerEntry.debit_amount)).filter(
            and_(
                LedgerEntry.ledger_type == LedgerType.CLIENT,
                LedgerEntry.date >= start_datetime,
                LedgerEntry.date <= end_datetime,
                LedgerEntry.transaction_type == TransactionType.PAYMENT_RECEIVED
            )
        ).scalar() or 0.0
        
        # Daily outgoing (payments made - debits to vendor ledgers)
        daily_outgoing = self.db.query(func.sum(LedgerEntry.debit_amount)).filter(
            and_(
                LedgerEntry.ledger_type == LedgerType.VENDOR,
                LedgerEntry.date >= start_datetime,
                LedgerEntry.date <= end_datetime,
                LedgerEntry.transaction_type == TransactionType.VENDOR_PAYMENT
            )
        ).scalar() or 0.0
        
        return {
            "daily_income": daily_income,
            "daily_outgoing": daily_outgoing,
            "daily_net": daily_income - daily_outgoing
        }
    
    def close(self):
        """Close database session"""
        if self.db:
            self.db.close()
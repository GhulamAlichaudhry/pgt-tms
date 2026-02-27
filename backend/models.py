from sqlalchemy import Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey, Text, Enum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"

class LedgerType(enum.Enum):
    CLIENT = "client"
    VENDOR = "vendor"
    CASH_BANK = "cash_bank"

class TransactionType(enum.Enum):
    RENT_RAISED = "rent_raised"
    PAYMENT_RECEIVED = "payment_received"
    VENDOR_CHARGE = "vendor_charge"
    VENDOR_PAYMENT = "vendor_payment"
    CASH_DEPOSIT = "cash_deposit"
    CASH_WITHDRAWAL = "cash_withdrawal"
    ADJUSTMENT = "adjustment"

class ReceivableStatus(enum.Enum):
    PENDING = "pending"
    PARTIALLY_PAID = "partially_paid"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"

class CollectionChannel(enum.Enum):
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    CHEQUE = "cheque"
    ONLINE_TRANSFER = "online_transfer"
    MOBILE_BANKING = "mobile_banking"
    CREDIT_CARD = "credit_card"

class PaymentRequestStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    PAID = "paid"
    CANCELLED = "cancelled"

class PaymentChannel(enum.Enum):
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"
    CHEQUE = "cheque"
    ONLINE_TRANSFER = "online_transfer"
    MOBILE_BANKING = "mobile_banking"

class PaymentType(enum.Enum):
    FULL = "full"
    PARTIAL = "partial"

# ============================================
# CASH REGISTER ENUMS (TASK 1)
# ============================================

class CashDirection(enum.Enum):
    """Cash flow direction - IN or OUT"""
    IN = "IN"   # Money coming in (client payments)
    OUT = "OUT"  # Money going out (vendor payments, expenses, salaries)

class CashSourceModule(enum.Enum):
    """Source module for cash transactions"""
    RECEIVABLE = "receivable"  # Client payment
    PAYABLE = "payable"  # Vendor payment (NOT an expense - cost already in trip)
    EXPENSE = "expense"  # Operating expense (office, fuel, maintenance, etc.)
    PAYROLL = "payroll"  # Salary payment
    ADJUSTMENT = "adjustment"  # Admin adjustment only

class PaymentMode(enum.Enum):
    """Payment modes"""
    CASH = "cash"
    BANK = "bank"
    CHEQUE = "cheque"
    ONLINE = "online"
    MOBILE = "mobile"

class TripStatus(enum.Enum):
    """Trip lifecycle status (TASK 3)"""
    DRAFT = "draft"  # Can be edited
    ACTIVE = "active"  # In progress
    COMPLETED = "completed"  # Finished, financial values locked
    LOCKED = "locked"  # Fully read-only, admin override only
    CANCELLED = "cancelled"  # Trip cancelled, financials reversed

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    role = Column(Enum(UserRole))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ============================================
# CENTRAL CASH REGISTER (TASK 1 - MOST IMPORTANT)
# ============================================

class CashTransaction(Base):
    """
    Central Cash Register - Single Source of Truth for ALL cash movements
    
    MANDATORY RULES:
    - No direct UI entry except admin adjustments
    - Every payment event MUST insert a record here
    - Vendor payments are NOT expenses (cost already captured at trip creation)
    """
    __tablename__ = "cash_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    amount = Column(Float, nullable=False)  # Always positive
    direction = Column(Enum(CashDirection), nullable=False, index=True)  # IN or OUT
    source_module = Column(Enum(CashSourceModule), nullable=False, index=True)
    source_id = Column(Integer, nullable=False, index=True)  # ID of source record
    payment_mode = Column(Enum(PaymentMode), nullable=False)
    reference = Column(String)  # Invoice/receipt number
    note = Column(Text)
    
    # Audit fields (TASK 8)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Soft delete (TASK 8)
    is_deleted = Column(Boolean, default=False)
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by])
    deleted_by_user = relationship("User", foreign_keys=[deleted_by])
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_cash_date', 'date'),
        Index('idx_cash_direction', 'direction'),
        Index('idx_cash_source', 'source_module', 'source_id'),
    )


class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    ledger_type = Column(Enum(LedgerType), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)  # client_id, vendor_id, or cash_account_id
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    description = Column(String, nullable=False)
    debit_amount = Column(Float, default=0.0, nullable=False)
    credit_amount = Column(Float, default=0.0, nullable=False)
    running_balance = Column(Float, nullable=False)  # Calculated field
    reference_no = Column(String, index=True)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_immutable = Column(Boolean, default=True)  # Prevents modification after creation
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by])
    
    # Composite indexes for performance
    __table_args__ = (
        Index('idx_ledger_entity_date', 'ledger_type', 'entity_id', 'date'),
        Index('idx_ledger_reference', 'reference_no'),
        Index('idx_ledger_transaction_type', 'transaction_type'),
    )

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    client_code = Column(String, unique=True, index=True)  # Auto-generated unique identifier
    name = Column(String, nullable=False, index=True)
    contact_person = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(Text)
    
    # Financial fields (calculated from ledger)
    current_balance = Column(Float, default=0.0)  # Calculated from ledger entries
    credit_limit = Column(Float, default=0.0)
    payment_terms = Column(Integer, default=30)  # Days
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ledger_entries = relationship("LedgerEntry", 
                                primaryjoin="and_(LedgerEntry.ledger_type=='client', LedgerEntry.entity_id==Client.id)",
                                foreign_keys="[LedgerEntry.entity_id]",
                                viewonly=True)
    agreements = relationship("ClientAgreement", back_populates="client")

class ClientAgreement(Base):
    __tablename__ = "client_agreements"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    agreement_reference = Column(String, unique=True, index=True)
    agreement_type = Column(String)  # Transport, Logistics, etc.
    start_date = Column(Date)
    end_date = Column(Date)
    terms_and_conditions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    client = relationship("Client", back_populates="agreements")

class Staff(Base):
    __tablename__ = "staff"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    gross_salary = Column(Float)
    advance_balance = Column(Float, default=0.0)
    monthly_deduction = Column(Float, default=0.0)
    
    # Director's Rule #1: Staff Advance Recovery fields
    recovery_start_date = Column(DateTime(timezone=True), nullable=True)
    advance_given_date = Column(DateTime(timezone=True), nullable=True)
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    payroll_entries = relationship("PayrollEntry", back_populates="staff")

class Vehicle(Base):
    __tablename__ = "vehicles"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_no = Column(String, unique=True, index=True)
    vehicle_type = Column(String)
    capacity_tons = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    trips = relationship("Trip", back_populates="vehicle")

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User Input Fields (Generic)
    date = Column(DateTime(timezone=True))
    reference_no = Column(String, unique=True, index=True)  # Trip/Job/Task reference
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    category_product = Column(String)  # Dynamic category/product
    source_location = Column(String)
    destination_location = Column(String)
    driver_operator = Column(String)  # Dynamic driver/operator
    
    # SMART SYSTEM: Client and Vendor Integration
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)  # Required for smart system
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)  # Required for smart system
    vendor_client = Column(String)    # Legacy field for display
    
    # SMART FINANCIAL FIELDS
    # Freight Mode
    freight_mode = Column(String, default="total")  # "total" or "per_ton"
    total_tonnage = Column(Float, nullable=False)  # Total cargo weight for all modes
    tonnage = Column(Float, nullable=True)  # Required when freight_mode = "per_ton" (for rate calculation)
    rate_per_ton = Column(Float, nullable=True)  # Rate per ton when using per_ton mode
    
    # CORE FINANCIAL DATA (User Input)
    vendor_freight = Column(Float, nullable=False)  # Amount to pay vendor (e.g., 30,000)
    client_freight = Column(Float, nullable=False)  # Amount to charge client (e.g., 40,000)
    
    # Additional Costs (Optional)
    local_shifting_charges = Column(Float, default=0.0)  # Local + Shifting charges (added to vendor freight)
    advance_paid = Column(Float, default=0.0)  # Advance given to driver/vendor
    fuel_cost = Column(Float, default=0.0)    # Fuel costs
    munshiyana_bank_charges = Column(Float, default=0.0)  # Bank charges, etc.
    other_expenses = Column(Float, default=0.0)  # Any other trip-related expenses
    
    # SMART AUTO CALCULATIONS (Read-only, computed by backend)
    # NOTE: Total vendor cost = vendor_freight + local_shifting_charges
    gross_profit = Column(Float)  # client_freight - (vendor_freight + local_shifting_charges)
    net_profit = Column(Float)    # gross_profit - (advance + fuel + munshiyana + other_expenses)
    profit_margin = Column(Float) # (net_profit / client_freight) * 100
    
    # SMART INTEGRATION FLAGS
    receivable_created = Column(Boolean, default=False)  # Auto-created receivable
    payable_created = Column(Boolean, default=False)    # Auto-created payable
    receivable_id = Column(Integer, ForeignKey("receivables.id"), nullable=True)
    payable_id = Column(Integer, ForeignKey("payables.id"), nullable=True)
    
    # TASK 3: Trip Lifecycle Status
    status = Column(Enum(TripStatus), default=TripStatus.DRAFT, nullable=False, index=True)
    # DRAFT → ACTIVE → COMPLETED → LOCKED
    # COMPLETED: Financial values locked, cannot change
    # LOCKED: Fully read-only, admin override only
    
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    locked_at = Column(DateTime(timezone=True), nullable=True)
    locked_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Soft delete (TASK 8)
    is_deleted = Column(Boolean, default=False)
    deleted_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    vehicle = relationship("Vehicle", back_populates="trips")
    client = relationship("Client", foreign_keys=[client_id])
    vendor = relationship("Vendor", foreign_keys=[vendor_id])
    receivable = relationship("Receivable", foreign_keys=[receivable_id])
    payable = relationship("Payable", foreign_keys=[payable_id])
    financial_transactions = relationship("FinancialTransaction", foreign_keys="FinancialTransaction.job_id")
    
    # Properties for display names
    @property
    def client_name(self):
        return self.client.name if self.client else None
    
    @property
    def vendor_name(self):
        return self.vendor.name if self.vendor else None
    
    @property
    def vehicle_number(self):
        return self.vehicle.vehicle_no if self.vehicle else None

class PayrollEntry(Base):
    __tablename__ = "payroll_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"))
    month = Column(Integer)  # 1-12
    year = Column(Integer)
    gross_salary = Column(Float)
    arrears = Column(Float, default=0.0)
    advance_deduction = Column(Float, default=0.0)
    other_deductions = Column(Float, default=0.0)
    net_payable = Column(Float)  # Calculated field
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    staff = relationship("Staff", back_populates="payroll_entries")

class StaffAdvanceLedger(Base):
    """
    Director's Rule #1: Smart Ledger for Staff Advance Tracking
    Handles multiple advances and recovery with complete audit trail
    """
    __tablename__ = "staff_advance_ledger"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("staff.id"), nullable=False)
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    transaction_type = Column(String, nullable=False)  # 'advance_given', 'recovery', 'adjustment'
    amount = Column(Float, nullable=False)  # Positive for advance given, negative for recovery
    balance_after = Column(Float, nullable=False)  # Running balance after this transaction
    description = Column(Text)
    payroll_id = Column(Integer, ForeignKey("payroll_entries.id"), nullable=True)  # Link to payroll if recovery
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    staff = relationship("Staff", foreign_keys=[staff_id])
    payroll = relationship("PayrollEntry", foreign_keys=[payroll_id])
    created_by_user = relationship("User", foreign_keys=[created_by])

class Vendor(Base):
    __tablename__ = "vendors"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_code = Column(String, unique=True, index=True)  # Auto-generated unique identifier
    name = Column(String, index=True, nullable=False)
    contact_person = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(Text)
    
    # Financial fields (calculated from ledger)
    current_balance = Column(Float, default=0.0)  # Calculated from ledger entries
    payment_terms = Column(Integer, default=30)  # Days
    tax_id = Column(String)
    
    # Status and metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    ledger_entries = relationship("LedgerEntry",
                                primaryjoin="and_(LedgerEntry.ledger_type=='vendor', LedgerEntry.entity_id==Vendor.id)",
                                foreign_keys="[LedgerEntry.entity_id]",
                                viewonly=True)
    contracts = relationship("VendorContract", back_populates="vendor")

class VendorContract(Base):
    __tablename__ = "vendor_contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    contract_reference = Column(String, unique=True, index=True)
    contract_type = Column(String)  # Service, Supply, etc.
    start_date = Column(Date)
    end_date = Column(Date)
    terms_and_conditions = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    vendor = relationship("Vendor", back_populates="contracts")

class FinancialTransaction(Base):
    __tablename__ = "financial_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime(timezone=True), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    reference_no = Column(String, index=True)
    
    # Polymorphic relationships
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    job_id = Column(Integer, ForeignKey("trips.id"), nullable=True)  # Links to Trip/Job
    
    # Audit fields
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    client = relationship("Client", foreign_keys=[client_id])
    vendor = relationship("Vendor", foreign_keys=[vendor_id])
    job = relationship("Trip", foreign_keys=[job_id])
    created_by_user = relationship("User", foreign_keys=[created_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])

class CashBankAccount(Base):
    __tablename__ = "cash_bank_accounts"
    
    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, nullable=False)
    account_type = Column(String, nullable=False)  # cash, bank
    account_number = Column(String)
    bank_name = Column(String)
    current_balance = Column(Float, default=0.0)  # Calculated from ledger
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    ledger_entries = relationship("LedgerEntry",
                                primaryjoin="and_(LedgerEntry.ledger_type=='cash_bank', LedgerEntry.entity_id==CashBankAccount.id)",
                                foreign_keys="[LedgerEntry.entity_id]",
                                viewonly=True)

class VehicleLog(Base):
    __tablename__ = "vehicle_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User Input Fields
    date = Column(Date)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    opening_meter_reading = Column(Float)
    closing_meter_reading = Column(Float)
    fuel_issued_quantity = Column(Float)  # Liters/Gallons
    
    # Auto Calculations (Read-only)
    distance_covered = Column(Float)  # closing - opening
    fuel_efficiency = Column(Float)   # distance / fuel (optional)
    
    # Metadata
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    vehicle = relationship("Vehicle", backref="vehicle_logs")

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # User Input Fields (Generic)
    date = Column(DateTime(timezone=True))
    expense_category = Column(String)  # Dynamic categories
    expense_type = Column(String, default="operational")  # operational, vendor
    description = Column(String)
    amount = Column(Float)
    
    # Optional associations
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    
    # Approval and audit
    receipt_image = Column(String, nullable=True)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approval_status = Column(String, default="pending")  # pending, approved, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    vehicle = relationship("Vehicle", backref="expenses")
    vendor = relationship("Vendor", backref="expenses")
    client = relationship("Client", backref="expenses")
    approved_by_user = relationship("User", foreign_keys=[approved_by])
    created_by_user = relationship("User", foreign_keys=[created_by])

class OfficeExpense(Base):
    """Office Expenses Tracking - Separate from operational expenses"""
    __tablename__ = "office_expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    entry_type = Column(String, nullable=False)  # 'expense' or 'cash_received'
    account_title = Column(String, nullable=False)  # Category or "Cash Received"
    particulars = Column(Text, nullable=False)  # Description
    amount_received = Column(Float, default=0.0)
    amount_paid = Column(Float, default=0.0)
    
    # Link to CEO Capital
    ceo_capital_transaction_id = Column(Integer, ForeignKey("ceo_capital.id"), nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by])
    ceo_capital_transaction = relationship("CEOCapital", foreign_keys=[ceo_capital_transaction_id])

class CEOCapital(Base):
    """CEO Capital Account - Tracks CEO's personal money from business profit"""
    __tablename__ = "ceo_capital"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False, index=True)
    transaction_type = Column(String, nullable=False)  # 'profit_allocation', 'office_expense', 'salary_payment', 'withdrawal', 'opening_balance'
    description = Column(Text, nullable=False)
    amount_in = Column(Float, default=0.0)  # Money coming in (profit, returns)
    amount_out = Column(Float, default=0.0)  # Money going out (expenses, salaries, withdrawals)
    balance = Column(Float, nullable=False)  # Running balance after this transaction
    
    # Reference to source transaction
    reference_id = Column(Integer, nullable=True)  # ID of related record
    reference_type = Column(String, nullable=True)  # 'trip', 'office_expense', 'payroll', 'withdrawal'
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    notes = Column(Text, nullable=True)
    
    # Relationships
    created_by_user = relationship("User", foreign_keys=[created_by])

class Receivable(Base):
    __tablename__ = "receivables"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Core receivable information
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)  # Link to originating trip
    invoice_number = Column(String, unique=True, index=True)
    description = Column(String, nullable=False)
    
    # Financial details
    total_amount = Column(Float, nullable=False)  # Total amount client owes
    paid_amount = Column(Float, default=0.0)  # Amount already collected
    remaining_amount = Column(Float, nullable=False)  # Outstanding balance
    
    # Dates and status
    invoice_date = Column(DateTime(timezone=True), nullable=False)
    due_date = Column(DateTime(timezone=True), nullable=False)
    status = Column(Enum(ReceivableStatus), default=ReceivableStatus.PENDING)
    
    # Payment tracking
    last_payment_date = Column(DateTime(timezone=True), nullable=True)
    payment_terms = Column(Integer, default=30)  # Days
    
    # Invoice PDF management (NEW)
    invoice_pdf_path = Column(String, nullable=True)
    invoice_generated_at = Column(DateTime(timezone=True), nullable=True)
    invoice_sent_at = Column(DateTime(timezone=True), nullable=True)
    invoice_template = Column(String, default='standard')
    
    # Invoice customization (NEW)
    custom_notes = Column(Text, nullable=True)
    discount_amount = Column(Float, default=0.0)
    discount_percentage = Column(Float, default=0.0)
    tax_amount = Column(Float, default=0.0)
    tax_percentage = Column(Float, default=0.0)
    
    # Approval workflow (NEW)
    requires_approval = Column(Boolean, default=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    approval_status = Column(String, default='approved')
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    client = relationship("Client", foreign_keys=[client_id])
    trip = relationship("Trip", foreign_keys=[trip_id])
    created_by_user = relationship("User", foreign_keys=[created_by])
    collections = relationship("Collection", back_populates="receivable")

class Collection(Base):
    __tablename__ = "collections"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Core collection information
    receivable_id = Column(Integer, ForeignKey("receivables.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    
    # Collection details
    collection_amount = Column(Float, nullable=False)
    collection_date = Column(DateTime(timezone=True), nullable=False)
    collection_channel = Column(Enum(CollectionChannel), nullable=False)
    
    # Reference information
    reference_number = Column(String, nullable=True)  # Bank ref, cheque number, etc.
    notes = Column(Text, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    collected_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    receivable = relationship("Receivable", back_populates="collections")
    client = relationship("Client", foreign_keys=[client_id])
    collected_by_user = relationship("User", foreign_keys=[collected_by])

class Payable(Base):
    __tablename__ = "payables"
    
    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"))
    invoice_number = Column(String, unique=True, index=True)
    description = Column(String)
    amount = Column(Float)  # Total amount
    outstanding_amount = Column(Float)  # Amount still owed (reduces when payments are made)
    due_date = Column(DateTime(timezone=True))
    status = Column(String, default="pending")  # pending, approved, paid, overdue
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    vendor = relationship("Vendor", backref="payables")
    payment_requests = relationship("PaymentRequest", back_populates="payable")

class PaymentRequest(Base):
    __tablename__ = "payment_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    payable_id = Column(Integer, ForeignKey("payables.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    
    # Payment details
    payment_type = Column(Enum(PaymentType), nullable=False)  # full, partial
    requested_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)  # Auto-calculated
    payment_channel = Column(Enum(PaymentChannel), nullable=False)
    
    # Request details
    request_reason = Column(Text)
    urgency_level = Column(String, default="normal")  # low, normal, high, urgent
    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Approval workflow
    status = Column(Enum(PaymentRequestStatus), default=PaymentRequestStatus.PENDING)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    
    # Payment execution
    payment_reference = Column(String, nullable=True)  # Bank reference, cheque number, etc.
    payment_date = Column(DateTime(timezone=True), nullable=True)
    payment_notes = Column(Text, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    payable = relationship("Payable", back_populates="payment_requests")
    vendor = relationship("Vendor", foreign_keys=[vendor_id])
    requested_by_user = relationship("User", foreign_keys=[requested_by])
    approved_by_user = relationship("User", foreign_keys=[approved_by])


# ============================================
# PROFESSIONAL ENHANCEMENTS - AUDIT & SECURITY
# ============================================

# Audit Trail System
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String, nullable=False)  # create, update, delete, login, logout
    table_name = Column(String, nullable=False)
    record_id = Column(Integer, nullable=True)
    old_values = Column(Text, nullable=True)  # JSON string
    new_values = Column(Text, nullable=True)  # JSON string
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    description = Column(String, nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_audit_user_timestamp', 'user_id', 'timestamp'),
        Index('idx_audit_table_record', 'table_name', 'record_id'),
        Index('idx_audit_action', 'action'),
    )

# System Settings
class SystemSetting(Base):
    __tablename__ = "system_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    setting_key = Column(String, unique=True, nullable=False, index=True)
    setting_value = Column(Text, nullable=False)
    setting_type = Column(String, default="string")  # string, number, boolean, json
    description = Column(String, nullable=True)
    is_public = Column(Boolean, default=False)  # Can non-admin users see this?
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    updated_by_user = relationship("User", foreign_keys=[updated_by])

# User Session Management
class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    session_token = Column(String, unique=True, nullable=False, index=True)
    ip_address = Column(String, nullable=True)
    user_agent = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    last_activity = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_session_user_active', 'user_id', 'is_active'),
        Index('idx_session_expires', 'expires_at'),
    )

# Notification System
class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, default="info")  # info, warning, error, success
    is_read = Column(Boolean, default=False)
    link = Column(String, nullable=True)  # URL to navigate to
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    read_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    user = relationship("User", foreign_keys=[user_id])
    
    # Indexes
    __table_args__ = (
        Index('idx_notification_user_read', 'user_id', 'is_read'),
        Index('idx_notification_created', 'created_at'),
    )

# Company Settings (for branding)
class CompanySetting(Base):
    __tablename__ = "company_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, default="PGT International (Private) Limited")
    company_address = Column(Text, nullable=True)
    company_phone = Column(String, nullable=True)
    company_email = Column(String, nullable=True)
    company_website = Column(String, nullable=True)
    company_logo_url = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)
    registration_number = Column(String, nullable=True)
    fiscal_year_start_month = Column(Integer, default=1)  # 1-12
    default_currency = Column(String, default="PKR")
    date_format = Column(String, default="YYYY-MM-DD")
    time_zone = Column(String, default="Asia/Karachi")
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Relationships
    updated_by_user = relationship("User", foreign_keys=[updated_by])

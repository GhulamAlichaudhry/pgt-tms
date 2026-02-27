from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
from models import UserRole

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# User Update Schema
class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Password Reset Schema
class PasswordReset(BaseModel):
    new_password: str

# Staff Schemas
class StaffBase(BaseModel):
    employee_id: str
    name: str
    position: str
    gross_salary: float
    monthly_deduction: Optional[float] = 0.0

class StaffCreate(StaffBase):
    pass

class Staff(StaffBase):
    id: int
    advance_balance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Vehicle Schemas
class VehicleBase(BaseModel):
    vehicle_no: str
    vehicle_type: str
    capacity_tons: float

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Enhanced Trip Schemas (SMART SYSTEM)
class TripBase(BaseModel):
    # User Input Fields (Generic)
    date: datetime
    reference_no: str
    vehicle_id: int
    category_product: str
    source_location: str
    destination_location: str
    driver_operator: str
    
    # SMART SYSTEM: Required Client and Vendor
    client_id: int  # Required for automatic receivable
    vendor_id: int  # Required for automatic payable
    vendor_client: Optional[str] = None  # Legacy display field
    
    # SMART FINANCIAL FIELDS
    freight_mode: Optional[str] = "total"  # "total" or "per_ton"
    total_tonnage: float  # Total cargo weight for all modes
    tonnage: Optional[float] = None  # For per-ton rate calculation
    rate_per_ton: Optional[float] = None
    
    # CORE FINANCIAL DATA (User Input) - SMART SYSTEM
    vendor_freight: float  # Amount to pay vendor (e.g., 30,000)
    client_freight: float  # Amount to charge client (e.g., 40,000)
    
    # Additional Costs (Optional)
    local_shifting_charges: Optional[float] = 0.0  # Local + Shifting charges (added to vendor freight)
    advance_paid: Optional[float] = 0.0
    fuel_cost: Optional[float] = 0.0
    munshiyana_bank_charges: Optional[float] = 0.0
    other_expenses: Optional[float] = 0.0
    
    notes: Optional[str] = None

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    
    # SMART AUTO CALCULATIONS (Read-only)
    gross_profit: float  # client_freight - vendor_freight
    net_profit: float    # gross_profit - all expenses
    profit_margin: float # (net_profit / client_freight) * 100
    
    # SMART INTEGRATION STATUS
    receivable_created: bool
    payable_created: bool
    receivable_id: Optional[int] = None
    payable_id: Optional[int] = None
    
    # Status and metadata
    status: Optional[str] = None  # Will be converted from enum
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    # Display names from relationships
    client_name: Optional[str] = None
    vendor_name: Optional[str] = None
    vehicle_number: Optional[str] = None
    
    class Config:
        from_attributes = True

# Vehicle Log Schema
class VehicleLogBase(BaseModel):
    date: date
    vehicle_id: int
    opening_meter_reading: float
    closing_meter_reading: float
    fuel_issued_quantity: float
    notes: Optional[str] = None

class VehicleLogCreate(VehicleLogBase):
    pass

class VehicleLog(VehicleLogBase):
    id: int
    distance_covered: float  # Auto-calculated: closing - opening
    fuel_efficiency: float   # Auto-calculated: distance / fuel
    created_at: datetime
    class Config:
        from_attributes = True

# Updated Ledger Entry Schema
class LedgerEntryBase(BaseModel):
    date: datetime
    vendor_id: int
    description: str
    debit_amount: Optional[float] = 0.0
    credit_amount: Optional[float] = 0.0
    reference_no: Optional[str] = None
    transaction_type: Optional[str] = None

class LedgerEntryCreate(LedgerEntryBase):
    pass

class LedgerEntry(LedgerEntryBase):
    id: int
    running_balance: float  # Auto-calculated: previous_balance + credit - debit
    created_at: datetime
    vendor: "Vendor"
    
    class Config:
        from_attributes = True

# Payroll Schemas
class PayrollEntryBase(BaseModel):
    staff_id: int
    month: int
    year: int
    gross_salary: float
    arrears: Optional[float] = 0.0
    advance_deduction: Optional[float] = 0.0
    other_deductions: Optional[float] = 0.0

class PayrollEntryCreate(PayrollEntryBase):
    pass

class PayrollEntry(PayrollEntryBase):
    id: int
    net_payable: float
    is_paid: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Vendor Schemas
class VendorBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int
    current_balance: float
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Ledger Schemas
class LedgerEntryBase(BaseModel):
    vendor_id: int
    date: datetime
    description: str
    debit_amount: Optional[float] = 0.0
    credit_amount: Optional[float] = 0.0
    reference_no: Optional[str] = None

class LedgerEntryCreate(LedgerEntryBase):
    pass

class LedgerEntry(LedgerEntryBase):
    id: int
    balance: float
    created_at: datetime
    
    class Config:
        from_attributes = True

# Dashboard Schemas
class DashboardStats(BaseModel):
    monthly_profit: float
    outstanding_receivables: float
    active_fleet_count: int
    pending_payroll_count: int
    total_trips_this_month: int

# Expense Schemas
class ExpenseBase(BaseModel):
    date: datetime
    expense_category: str
    description: str
    amount: float
    vehicle_id: Optional[int] = None
    receipt_image: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    expense_type: Optional[str] = "operational"
    approved_by: Optional[int] = None
    approval_status: Optional[str] = "pending"
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

# Client Schemas
class ClientBase(BaseModel):
    name: str
    contact_person: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    credit_limit: Optional[float] = 0.0
    payment_terms: Optional[int] = 30

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    client_code: Optional[str] = None
    current_balance: float
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Receivable Schemas
class ReceivableBase(BaseModel):
    client_id: int
    trip_id: Optional[int] = None
    invoice_number: str
    description: str
    total_amount: float
    invoice_date: datetime
    due_date: datetime
    payment_terms: Optional[int] = 30

class ReceivableCreate(ReceivableBase):
    pass

class Receivable(ReceivableBase):
    id: int
    paid_amount: float
    remaining_amount: float
    status: str
    last_payment_date: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    client: Optional['Client'] = None  # Include client relationship
    
    class Config:
        from_attributes = True

# Collection Schemas
class CollectionBase(BaseModel):
    receivable_id: int
    collection_amount: float
    collection_date: datetime
    collection_channel: str
    reference_number: Optional[str] = None
    notes: Optional[str] = None

class CollectionCreate(CollectionBase):
    pass

class Collection(CollectionBase):
    id: int
    client_id: int
    created_at: datetime
    
    # Relationships
    receivable: "Receivable"
    client: "Client"
    collected_by_user: "User"
    
    class Config:
        from_attributes = True

# Payable Schemas
class PayableBase(BaseModel):
    vendor_id: int
    invoice_number: str
    description: str
    amount: float
    due_date: datetime
    status: Optional[str] = "pending"

class PayableCreate(PayableBase):
    pass

class Payable(PayableBase):
    id: int
    outstanding_amount: Optional[float] = None  # Add outstanding_amount field
    created_at: datetime
    paid_at: Optional[datetime] = None
    vendor: Optional['Vendor'] = None  # Include vendor relationship
    
    class Config:
        from_attributes = True

# Payment Request Schemas
class PaymentRequestBase(BaseModel):
    payable_id: int
    payment_type: str  # "full" or "partial"
    requested_amount: float
    payment_channel: str  # "bank_transfer", "cash", "cheque", etc.
    request_reason: Optional[str] = None
    urgency_level: Optional[str] = "normal"

class PaymentRequestCreate(PaymentRequestBase):
    pass

class PaymentRequestUpdate(BaseModel):
    status: Optional[str] = None
    rejection_reason: Optional[str] = None
    payment_reference: Optional[str] = None
    payment_notes: Optional[str] = None

class PaymentRequest(PaymentRequestBase):
    id: int
    vendor_id: int
    remaining_amount: float
    status: str
    requested_by: int
    requested_at: datetime
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None
    payment_reference: Optional[str] = None
    payment_date: Optional[datetime] = None
    payment_notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
    
# Authentication Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


# Office Expense Schemas
class OfficeExpenseBase(BaseModel):
    date: date
    entry_type: str  # 'expense' or 'cash_received'
    account_title: str
    particulars: str
    amount_received: Optional[float] = 0.0
    amount_paid: Optional[float] = 0.0

class OfficeExpenseCreate(OfficeExpenseBase):
    pass

class OfficeExpense(OfficeExpenseBase):
    id: int
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True


# CEO Capital Schemas
class CEOCapitalBase(BaseModel):
    date: date
    transaction_type: str
    description: str
    amount_in: Optional[float] = 0.0
    amount_out: Optional[float] = 0.0
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    notes: Optional[str] = None

class CEOCapitalCreate(CEOCapitalBase):
    pass

class CEOCapital(CEOCapitalBase):
    id: int
    balance: float
    created_at: datetime
    created_by: int
    
    class Config:
        from_attributes = True

class CEOCapitalBalance(BaseModel):
    current_balance: float
    total_in: float
    total_out: float
    last_transaction_date: Optional[date] = None

class CEOCapitalMonthlySummary(BaseModel):
    month: int
    year: int
    opening_balance: float
    total_profit: float
    total_expenses: float
    total_salaries: float
    total_withdrawals: float
    closing_balance: float
    transaction_count: int

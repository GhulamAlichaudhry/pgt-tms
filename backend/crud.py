from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, extract
import models
import schemas
from auth import get_password_hash
from datetime import datetime, date, timedelta
from audit_service import AuditService
from notification_service import NotificationService
from validators import Validator, BusinessValidator, ValidationError
from typing import Optional
from fastapi import Request

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Staff CRUD
def create_staff(db: Session, staff: schemas.StaffCreate):
    db_staff = models.Staff(**staff.model_dump())
    db.add(db_staff)
    db.commit()
    db.refresh(db_staff)
    return db_staff

def get_staff(db: Session, staff_id: int):
    return db.query(models.Staff).filter(models.Staff.id == staff_id).first()

def get_all_staff(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Staff).filter(models.Staff.is_active == True).offset(skip).limit(limit).all()

def update_staff_advance(db: Session, staff_id: int, advance_amount: float):
    staff = get_staff(db, staff_id)
    if staff:
        staff.advance_balance += advance_amount
        db.commit()
        db.refresh(staff)
    return staff

# Vehicle CRUD
def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.model_dump())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).filter(models.Vehicle.is_active == True).offset(skip).limit(limit).all()

def get_active_fleet_count(db: Session):
    return db.query(models.Vehicle).filter(models.Vehicle.is_active == True).count()

# SMART TRIP CRUD - One-Time Entry System
def create_trip(db: Session, trip: schemas.TripCreate, current_user_id: int = 1, request: Optional[Request] = None):
    """
    SMART SYSTEM: One trip entry automatically creates:
    1. Trip record with automatic profit calculations
    2. Receivable (Client owes Company)
    3. Payable (Company owes Vendor)
    
    Example: Vendor Freight = 30,000, Client Freight = 40,000, Company Profit = 10,000
    """
    
    # SMART CALCULATIONS
    # Handle per-ton calculation if freight_mode is "per_ton"
    if trip.freight_mode == "per_ton" and trip.tonnage and trip.rate_per_ton:
        # For per-ton mode: Only auto-calculate CLIENT freight
        # Vendor freight remains manual (lump sum deal)
        trip.client_freight = trip.tonnage * trip.rate_per_ton
        # vendor_freight is kept as provided by user (lump sum deal)
    
    # Auto Calculations for SMART SYSTEM
    # Total vendor cost includes vendor_freight + local_shifting_charges
    total_vendor_cost = trip.vendor_freight + (trip.local_shifting_charges or 0)
    gross_profit = trip.client_freight - total_vendor_cost  # Company's gross profit
    net_profit = gross_profit - (trip.advance_paid + trip.fuel_cost + trip.munshiyana_bank_charges + trip.other_expenses)
    profit_margin = (net_profit / trip.client_freight * 100) if trip.client_freight > 0 else 0
    
    # Create Trip with SMART calculations
    db_trip = models.Trip(
        **trip.model_dump(exclude={'gross_profit', 'net_profit', 'profit_margin'}),
        gross_profit=gross_profit,
        net_profit=net_profit,
        profit_margin=profit_margin,
        receivable_created=False,  # Will be set to True after creating receivable
        payable_created=False     # Will be set to True after creating payable
    )
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    
    # AUDIT LOGGING
    if request:
        audit = AuditService(db)
        from audit_service import get_client_ip, get_user_agent
        audit.log_create(
            user_id=current_user_id,
            table_name="trips",
            record_id=db_trip.id,
            new_values={
                "reference_no": db_trip.reference_no,
                "client_freight": db_trip.client_freight,
                "vendor_freight": db_trip.vendor_freight,
                "gross_profit": gross_profit,
                "net_profit": net_profit
            },
            ip_address=get_client_ip(request) if request else None,
            user_agent=get_user_agent(request) if request else None
        )
    
    # SMART SYSTEM: Automatically create RECEIVABLE (Client owes Company)
    try:
        # Generate invoice number for receivable
        invoice_number = f"INV-{db_trip.reference_no}-{datetime.now().strftime('%Y%m%d')}"
        
        receivable_data = schemas.ReceivableCreate(
            client_id=trip.client_id,
            trip_id=db_trip.id,
            invoice_number=invoice_number,
            description=f"Transportation service - {trip.category_product} from {trip.source_location} to {trip.destination_location}",
            total_amount=trip.client_freight,  # Amount client owes to company
            invoice_date=datetime.now(),
            due_date=datetime.now() + timedelta(days=30),
            payment_terms=30
        )
        
        receivable = create_receivable(db, receivable_data, current_user_id)
        
        # Link receivable to trip
        db_trip.receivable_id = receivable.id
        db_trip.receivable_created = True
        
        print(f"✅ SMART SYSTEM: Created receivable {receivable.id} for PKR {trip.client_freight:,.2f}")
        
    except Exception as e:
        print(f"❌ Warning: Failed to create receivable for trip {db_trip.id}: {e}")
    
    # SMART SYSTEM: Automatically create PAYABLE (Company owes Vendor)
    try:
        # Generate invoice number for payable
        payable_invoice = f"PAY-{db_trip.reference_no}-{datetime.now().strftime('%Y%m%d')}"
        
        # Total amount to pay vendor includes vendor_freight + local_shifting_charges
        total_payable_amount = trip.vendor_freight + (trip.local_shifting_charges or 0)
        
        payable_data = schemas.PayableCreate(
            vendor_id=trip.vendor_id,
            invoice_number=payable_invoice,
            description=f"Vehicle hire - {trip.category_product} transport service (Freight: PKR {trip.vendor_freight:,.0f} + Local/Shifting: PKR {trip.local_shifting_charges or 0:,.0f})",
            amount=total_payable_amount,  # Amount company owes to vendor (including local charges)
            due_date=datetime.now() + timedelta(days=15),  # Shorter payment terms for vendors
            status="pending"
        )
        
        payable = create_payable(db, payable_data)
        
        # Link payable to trip
        db_trip.payable_id = payable.id
        db_trip.payable_created = True
        
        print(f"✅ SMART SYSTEM: Created payable {payable.id} for PKR {total_payable_amount:,.2f} (Freight: {trip.vendor_freight:,.0f} + Local/Shifting: {trip.local_shifting_charges or 0:,.0f})")
        
    except Exception as e:
        print(f"❌ Warning: Failed to create payable for trip {db_trip.id}: {e}")
    
    # SMART SYSTEM: Automatically allocate profit to CEO Capital
    try:
        if net_profit > 0:  # Only allocate if there's actual profit
            # Get current CEO Capital balance
            last_ceo_transaction = db.query(models.CEOCapital).order_by(
                models.CEOCapital.date.desc(),
                models.CEOCapital.id.desc()
            ).first()
            
            current_balance = last_ceo_transaction.balance if last_ceo_transaction else 0.0
            new_balance = current_balance + net_profit
            
            # Create CEO Capital profit allocation transaction
            ceo_transaction = models.CEOCapital(
                date=db_trip.trip_date,
                transaction_type='profit_allocation',
                description=f"Trip Profit: {db_trip.reference_no} - {trip.category_product} ({trip.source_location} to {trip.destination_location})",
                amount_in=net_profit,
                amount_out=0.0,
                balance=new_balance,
                reference_id=db_trip.id,
                reference_type='trip',
                created_by=current_user_id
            )
            db.add(ceo_transaction)
            db.flush()
            
            print(f"✅ SMART SYSTEM: Allocated profit PKR {net_profit:,.2f} to CEO Capital (New Balance: PKR {new_balance:,.2f})")
        else:
            print(f"⚠️ SMART SYSTEM: No profit to allocate (Net Profit: PKR {net_profit:,.2f})")
            
    except Exception as e:
        print(f"❌ Warning: Failed to allocate profit to CEO Capital for trip {db_trip.id}: {e}")
    
    # Final commit with all smart integrations
    db.commit()
    db.refresh(db_trip)
    
    # SMART SYSTEM SUMMARY
    print(f"""
    🚀 SMART TRIP CREATED:
    📋 Trip: {db_trip.reference_no}
    💰 Client Freight: PKR {trip.client_freight:,.2f}
    💸 Vendor Freight: PKR {trip.vendor_freight:,.2f}
    📈 Gross Profit: PKR {gross_profit:,.2f}
    📊 Net Profit: PKR {net_profit:,.2f}
    📋 Receivable: {'✅ Created' if db_trip.receivable_created else '❌ Failed'}
    📋 Payable: {'✅ Created' if db_trip.payable_created else '❌ Failed'}
    💼 CEO Capital: {'✅ Profit Allocated' if net_profit > 0 else '⚠️ No Profit'}
    """)
    
    return db_trip

# Vehicle Log CRUD with Auto Calculations
def create_vehicle_log(db: Session, log: schemas.VehicleLogCreate):
    # Auto Calculations
    distance_covered = log.closing_meter_reading - log.opening_meter_reading
    fuel_efficiency = distance_covered / log.fuel_issued_quantity if log.fuel_issued_quantity > 0 else 0
    
    # Validation: Closing must be greater than Opening
    if log.closing_meter_reading <= log.opening_meter_reading:
        raise ValueError("Closing meter reading must be greater than opening reading")
    
    db_log = models.VehicleLog(
        **log.model_dump(),
        distance_covered=distance_covered,
        fuel_efficiency=fuel_efficiency
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

# Ledger Entry CRUD with Running Balance
def create_ledger_entry(db: Session, ledger: schemas.LedgerEntryCreate):
    # Get previous balance for this vendor
    last_entry = db.query(models.LedgerEntry).filter(
        models.LedgerEntry.vendor_id == ledger.vendor_id
    ).order_by(models.LedgerEntry.created_at.desc()).first()
    
    previous_balance = last_entry.running_balance if last_entry else 0.0
    
    # Auto Calculation: Running Balance = Previous Balance + Credit - Debit
    running_balance = previous_balance + ledger.credit_amount - ledger.debit_amount
    
    db_ledger = models.LedgerEntry(
        **ledger.model_dump(),
        running_balance=running_balance
    )
    db.add(db_ledger)
    db.commit()
    db.refresh(db_ledger)
    
    # Update vendor's current balance
    vendor = db.query(models.Vendor).filter(models.Vendor.id == ledger.vendor_id).first()
    if vendor:
        vendor.current_balance = running_balance
        db.commit()
    
    return db_ledger

def get_trips(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Trip).options(
        joinedload(models.Trip.client),
        joinedload(models.Trip.vendor),
        joinedload(models.Trip.vehicle)
    ).offset(skip).limit(limit).all()

def get_monthly_trips(db: Session, year: int, month: int):
    return db.query(models.Trip).filter(
        extract('year', models.Trip.date) == year,
        extract('month', models.Trip.date) == month
    ).all()

def get_monthly_profit(db: Session, year: int, month: int):
    result = db.query(func.sum(models.Trip.net_amount)).filter(
        extract('year', models.Trip.date) == year,
        extract('month', models.Trip.date) == month
    ).scalar()
    return result or 0.0

# Payroll CRUD
def create_payroll_entry(db: Session, payroll: schemas.PayrollEntryCreate):
    """
    Create payroll entry with automatic advance recovery
    Director's Rule #1: Auto-deduct monthly_deduction from staff advance
    """
    # Get staff to check for advance balance
    staff = get_staff(db, payroll.staff_id)
    if not staff:
        raise ValueError("Staff not found")
    
    # Auto-calculate advance deduction if staff has advance balance
    advance_deduction = payroll.advance_deduction
    if staff.advance_balance > 0 and staff.monthly_deduction > 0:
        # Use the configured monthly deduction
        advance_deduction = min(staff.monthly_deduction, staff.advance_balance)
    
    # Calculate net payable
    net_payable = payroll.gross_salary + payroll.arrears - advance_deduction - payroll.other_deductions
    
    db_payroll = models.PayrollEntry(
        staff_id=payroll.staff_id,
        month=payroll.month,
        year=payroll.year,
        gross_salary=payroll.gross_salary,
        arrears=payroll.arrears,
        advance_deduction=advance_deduction,
        other_deductions=payroll.other_deductions,
        net_payable=net_payable,
        is_paid=payroll.is_paid
    )
    db.add(db_payroll)
    db.flush()  # Get the payroll ID
    
    # Update staff advance balance and create ledger entry
    if advance_deduction > 0 and staff.advance_balance > 0:
        current_balance = staff.advance_balance
        new_balance = current_balance - advance_deduction
        
        # Create ledger entry for recovery
        ledger_entry = models.StaffAdvanceLedger(
            staff_id=staff.id,
            transaction_date=datetime.now(),
            transaction_type='recovery',
            amount=-advance_deduction,  # Negative for recovery
            balance_after=new_balance,
            description=f"Payroll recovery - {payroll.month}/{payroll.year}",
            payroll_id=db_payroll.id,
            created_by=1  # System/Admin user
        )
        db.add(ledger_entry)
        
        # Update staff balance
        staff.advance_balance = new_balance
    
    db.commit()
    db.refresh(db_payroll)
    return db_payroll

def get_payroll_entries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.PayrollEntry).offset(skip).limit(limit).all()

def get_pending_payroll_count(db: Session):
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Count staff who don't have payroll entry for current month
    staff_count = db.query(models.Staff).filter(models.Staff.is_active == True).count()
    payroll_count = db.query(models.PayrollEntry).filter(
        models.PayrollEntry.month == current_month,
        models.PayrollEntry.year == current_year
    ).count()
    
    return staff_count - payroll_count

# Vendor CRUD
def create_vendor(db: Session, vendor: schemas.VendorCreate):
    db_vendor = models.Vendor(**vendor.model_dump())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vendor).filter(models.Vendor.is_active == True).offset(skip).limit(limit).all()

def get_outstanding_receivables(db: Session):
    result = db.query(func.sum(models.Vendor.current_balance)).filter(
        models.Vendor.current_balance > 0
    ).scalar()
    return result or 0.0

# Ledger CRUD
def create_ledger_entry(db: Session, ledger: schemas.LedgerEntryCreate):
    # Get vendor's current balance
    vendor = db.query(models.Vendor).filter(models.Vendor.id == ledger.vendor_id).first()
    if not vendor:
        return None
    
    # Calculate new balance
    balance_change = ledger.debit_amount - ledger.credit_amount
    new_balance = vendor.current_balance + balance_change
    
    db_ledger = models.LedgerEntry(
        **ledger.model_dump(),
        balance=new_balance
    )
    db.add(db_ledger)
    
    # Update vendor balance
    vendor.current_balance = new_balance
    
    db.commit()
    db.refresh(db_ledger)
    return db_ledger

def get_ledger_entries(db: Session, vendor_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.LedgerEntry).filter(
        models.LedgerEntry.vendor_id == vendor_id
    ).offset(skip).limit(limit).all()

# Dashboard Stats
def get_dashboard_stats(db: Session):
    current_date = datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    
    monthly_profit = get_monthly_profit(db, current_year, current_month)
    outstanding_receivables = get_outstanding_receivables(db)
    active_fleet_count = get_active_fleet_count(db)
    pending_payroll_count = get_pending_payroll_count(db)
    
    total_trips_this_month = db.query(models.Trip).filter(
        extract('year', models.Trip.date) == current_year,
        extract('month', models.Trip.date) == current_month
    ).count()
    
    return schemas.DashboardStats(
        monthly_profit=monthly_profit,
        outstanding_receivables=outstanding_receivables,
        active_fleet_count=active_fleet_count,
        pending_payroll_count=pending_payroll_count,
        total_trips_this_month=total_trips_this_month
    )

# Expense CRUD
def create_expense(db: Session, expense: schemas.ExpenseCreate, current_user_id: int = 1):
    db_expense = models.Expense(
        **expense.model_dump(),
        created_by=current_user_id
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Expense).offset(skip).limit(limit).all()

def get_expense(db: Session, expense_id: int):
    return db.query(models.Expense).filter(models.Expense.id == expense_id).first()

# Client CRUD
def create_client(db: Session, client: schemas.ClientCreate):
    # Generate client code
    client_count = db.query(models.Client).count()
    client_code = f"CLI-{client_count + 1:04d}"
    
    db_client = models.Client(
        **client.model_dump(),
        client_code=client_code,
        current_balance=0.0
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Client).filter(models.Client.is_active == True).offset(skip).limit(limit).all()

def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

# Receivable CRUD
def create_receivable(db: Session, receivable: schemas.ReceivableCreate, current_user_id: int):
    # Calculate remaining amount (initially equals total amount)
    remaining_amount = receivable.total_amount
    
    db_receivable = models.Receivable(
        **receivable.model_dump(),
        paid_amount=0.0,
        remaining_amount=remaining_amount,
        created_by=current_user_id
    )
    db.add(db_receivable)
    db.commit()
    db.refresh(db_receivable)
    
    # Update client's current balance (increase receivable)
    client = db.query(models.Client).filter(models.Client.id == receivable.client_id).first()
    if client:
        client.current_balance += receivable.total_amount
        db.commit()
    
    return db_receivable

def get_receivables(db: Session, skip: int = 0, limit: int = 100, client_id: int = None, status: str = None):
    query = db.query(models.Receivable).options(
        joinedload(models.Receivable.client)
    )
    if client_id:
        query = query.filter(models.Receivable.client_id == client_id)
    if status:
        query = query.filter(models.Receivable.status == status)
    return query.order_by(models.Receivable.created_at.desc()).offset(skip).limit(limit).all()

def get_receivable(db: Session, receivable_id: int):
    return db.query(models.Receivable).options(
        joinedload(models.Receivable.client)
    ).filter(models.Receivable.id == receivable_id).first()

def create_collection(db: Session, collection: schemas.CollectionCreate, current_user_id: int):
    # Get the receivable
    receivable = get_receivable(db, collection.receivable_id)
    if not receivable:
        raise ValueError("Receivable not found")
    
    # Validate collection amount
    if collection.collection_amount > receivable.remaining_amount:
        raise ValueError("Collection amount cannot exceed remaining balance")
    
    # Convert collection channel string to enum
    channel_enum = {
        "bank_transfer": models.CollectionChannel.BANK_TRANSFER,
        "cash": models.CollectionChannel.CASH,
        "cheque": models.CollectionChannel.CHEQUE,
        "online_transfer": models.CollectionChannel.ONLINE_TRANSFER,
        "mobile_banking": models.CollectionChannel.MOBILE_BANKING,
        "credit_card": models.CollectionChannel.CREDIT_CARD
    }.get(collection.collection_channel, models.CollectionChannel.BANK_TRANSFER)
    
    # Create collection record
    db_collection = models.Collection(
        receivable_id=collection.receivable_id,
        client_id=receivable.client_id,
        collection_amount=collection.collection_amount,
        collection_date=collection.collection_date,
        collection_channel=channel_enum,
        reference_number=collection.reference_number,
        notes=collection.notes,
        collected_by=current_user_id
    )
    db.add(db_collection)
    
    # Update receivable amounts
    receivable.paid_amount += collection.collection_amount
    receivable.remaining_amount -= collection.collection_amount
    receivable.last_payment_date = collection.collection_date
    
    # Update receivable status
    if receivable.remaining_amount <= 0:
        receivable.status = models.ReceivableStatus.PAID
    elif receivable.paid_amount > 0:
        receivable.status = models.ReceivableStatus.PARTIALLY_PAID
    
    # Update client balance (reduce receivable)
    client = db.query(models.Client).filter(models.Client.id == receivable.client_id).first()
    if client:
        client.current_balance -= collection.collection_amount
    
    db.commit()
    db.refresh(db_collection)
    return db_collection

def get_collections(db: Session, skip: int = 0, limit: int = 100, receivable_id: int = None):
    query = db.query(models.Collection)
    if receivable_id:
        query = query.filter(models.Collection.receivable_id == receivable_id)
    return query.order_by(models.Collection.created_at.desc()).offset(skip).limit(limit).all()

def create_receivable_from_trip(db: Session, trip: models.Trip, current_user_id: int):
    """Automatically create receivable when trip is completed"""
    if not trip.client_id or trip.receivable_created:
        return None
    
    # Generate invoice number
    invoice_number = f"INV-{trip.reference_no}-{datetime.now().strftime('%Y%m%d')}"
    
    # Create receivable
    receivable_data = schemas.ReceivableCreate(
        client_id=trip.client_id,
        trip_id=trip.id,
        invoice_number=invoice_number,
        description=f"Transportation service - {trip.category_product} from {trip.source_location} to {trip.destination_location}",
        total_amount=trip.gross_amount,
        invoice_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=30),
        payment_terms=30
    )
    
    receivable = create_receivable(db, receivable_data, current_user_id)
    
    # Mark trip as having receivable created
    trip.receivable_created = True
    trip.receivable_amount = trip.gross_amount
    db.commit()
    
    return receivable

# Payable CRUD
def create_payable(db: Session, payable: schemas.PayableCreate):
    db_payable = models.Payable(
        **payable.model_dump(),
        outstanding_amount=payable.amount  # Initially, outstanding = total amount
    )
    db.add(db_payable)
    db.commit()
    db.refresh(db_payable)
    return db_payable

def get_payables(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Payable).options(
        joinedload(models.Payable.vendor)
    ).offset(skip).limit(limit).all()

def get_payable(db: Session, payable_id: int):
    return db.query(models.Payable).options(
        joinedload(models.Payable.vendor)
    ).filter(models.Payable.id == payable_id).first()

def update_payable_status(db: Session, payable_id: int, status: str):
    payable = get_payable(db, payable_id)
    if payable:
        payable.status = status
        if status == "paid":
            payable.paid_at = datetime.now()
        db.commit()
        db.refresh(payable)
    return payable

# Payment Request CRUD
def create_payment_request(db: Session, payment_request: schemas.PaymentRequestCreate, current_user_id: int):
    # Get the payable to calculate remaining amount
    payable = get_payable(db, payment_request.payable_id)
    if not payable:
        raise ValueError("Payable not found")
    
    # Calculate remaining amount
    if payment_request.payment_type == "full":
        remaining_amount = 0.0
    else:  # partial
        remaining_amount = payable.amount - payment_request.requested_amount
    
    # Convert string enums to enum types
    payment_type_enum = models.PaymentType.FULL if payment_request.payment_type == "full" else models.PaymentType.PARTIAL
    
    payment_channel_enum = {
        "bank_transfer": models.PaymentChannel.BANK_TRANSFER,
        "cash": models.PaymentChannel.CASH,
        "cheque": models.PaymentChannel.CHEQUE,
        "online_transfer": models.PaymentChannel.ONLINE_TRANSFER,
        "mobile_banking": models.PaymentChannel.MOBILE_BANKING
    }.get(payment_request.payment_channel, models.PaymentChannel.BANK_TRANSFER)
    
    db_payment_request = models.PaymentRequest(
        payable_id=payment_request.payable_id,
        vendor_id=payable.vendor_id,
        payment_type=payment_type_enum,
        requested_amount=payment_request.requested_amount,
        remaining_amount=remaining_amount,
        payment_channel=payment_channel_enum,
        request_reason=payment_request.request_reason,
        urgency_level=payment_request.urgency_level,
        requested_by=current_user_id
    )
    db.add(db_payment_request)
    db.commit()
    db.refresh(db_payment_request)
    return db_payment_request

def get_payment_requests(db: Session, skip: int = 0, limit: int = 100, status: str = None):
    query = db.query(models.PaymentRequest).options(
        joinedload(models.PaymentRequest.vendor),
        joinedload(models.PaymentRequest.payable)
    )
    if status:
        query = query.filter(models.PaymentRequest.status == status)
    return query.order_by(models.PaymentRequest.requested_at.desc()).offset(skip).limit(limit).all()

def get_payment_request(db: Session, request_id: int):
    return db.query(models.PaymentRequest).filter(models.PaymentRequest.id == request_id).first()

def update_payment_request(db: Session, request_id: int, update_data: schemas.PaymentRequestUpdate, current_user_id: int):
    payment_request = get_payment_request(db, request_id)
    if not payment_request:
        return None
    
    # Handle status enum conversion
    if update_data.status:
        status_enum = {
            "pending": models.PaymentRequestStatus.PENDING,
            "approved": models.PaymentRequestStatus.APPROVED,
            "rejected": models.PaymentRequestStatus.REJECTED,
            "paid": models.PaymentRequestStatus.PAID,
            "cancelled": models.PaymentRequestStatus.CANCELLED
        }.get(update_data.status, models.PaymentRequestStatus.PENDING)
        payment_request.status = status_enum
    
    # Update other fields
    if update_data.rejection_reason:
        payment_request.rejection_reason = update_data.rejection_reason
    if update_data.payment_reference:
        payment_request.payment_reference = update_data.payment_reference
    if update_data.payment_notes:
        payment_request.payment_notes = update_data.payment_notes
    
    # Handle status changes
    if update_data.status == "approved":
        payment_request.approved_by = current_user_id
        payment_request.approved_at = datetime.now()
    elif update_data.status == "paid":
        payment_request.payment_date = datetime.now()
        
        # Get the payable
        payable = payment_request.payable
        
        # CRITICAL FIX: Initialize outstanding_amount if it's None
        if payable.outstanding_amount is None:
            payable.outstanding_amount = payable.amount
        
        # Reduce outstanding_amount when payment is made
        payable.outstanding_amount -= payment_request.requested_amount
        
        # Update the related payable status
        if payment_request.payment_type == models.PaymentType.FULL or payable.outstanding_amount <= 0:
            payable.status = "paid"
            payable.paid_at = datetime.now()
            payable.outstanding_amount = 0  # Ensure it's exactly 0
        else:
            payable.status = "partially_paid"
        
        # Update vendor balance (reduce the payable amount)
        vendor = db.query(models.Vendor).filter(models.Vendor.id == payment_request.vendor_id).first()
        if vendor:
            vendor.current_balance -= payment_request.requested_amount
        
        db.commit()
        db.refresh(payment_request)
        
        # TASK 2.2: CASH REGISTER INTEGRATION - Record vendor payment
        from cash_register_service import CashRegisterService
        cash_register = CashRegisterService(db)
        cash_register.record_vendor_payment(payment_request, current_user_id)
        
        return payment_request
    
    db.commit()
    db.refresh(payment_request)
    return payment_request

def get_pending_payment_requests_count(db: Session):
    return db.query(models.PaymentRequest).filter(
        models.PaymentRequest.status == models.PaymentRequestStatus.PENDING
    ).count()
# Vehicle Log CRUD functions
def get_vehicle_logs(db: Session, skip: int = 0, limit: int = 100, vehicle_id: int = None):
    query = db.query(models.VehicleLog)
    if vehicle_id:
        query = query.filter(models.VehicleLog.vehicle_id == vehicle_id)
    return query.offset(skip).limit(limit).all()

def get_vehicle_log(db: Session, log_id: int):
    return db.query(models.VehicleLog).filter(models.VehicleLog.id == log_id).first()

# Summary & Reporting functions
def get_summary_report(db: Session, start_date: str = None, end_date: str = None):
    """Generate summary report with key metrics"""
    
    # Base queries
    trips_query = db.query(models.Trip)
    expenses_query = db.query(models.Expense)
    
    # Apply date filters if provided
    if start_date and end_date:
        trips_query = trips_query.filter(models.Trip.date.between(start_date, end_date))
        expenses_query = expenses_query.filter(models.Expense.date.between(start_date, end_date))
    
    # Calculate aggregations
    trips = trips_query.all()
    expenses = expenses_query.all()
    
    total_gross_revenue = sum(trip.gross_amount for trip in trips)
    total_advances = sum(trip.advance_paid for trip in trips)
    total_fuel_costs = sum(trip.fuel_cost for trip in trips)
    total_munshiyana_charges = sum(trip.munshiyana_bank_charges for trip in trips)
    total_net_amount = sum(trip.net_amount for trip in trips)
    
    total_office_expenses = sum(expense.amount for expense in expenses)
    
    # Net Result = Total Net Amount - Office Expenses
    net_result = total_net_amount - total_office_expenses
    
    return {
        "period": {"start_date": start_date, "end_date": end_date},
        "operations": {
            "total_gross_revenue": total_gross_revenue,
            "total_advances": total_advances,
            "total_fuel_costs": total_fuel_costs,
            "total_munshiyana_charges": total_munshiyana_charges,
            "total_net_amount": total_net_amount
        },
        "expenses": {
            "total_office_expenses": total_office_expenses
        },
        "net_result": net_result,
        "trip_count": len(trips),
        "expense_count": len(expenses)
    }

def get_profit_loss_report(db: Session, start_date: str = None, end_date: str = None):
    """Generate detailed profit & loss report"""
    
    summary = get_summary_report(db, start_date, end_date)
    
    # Get expense breakdown by category
    expenses_query = db.query(models.Expense)
    if start_date and end_date:
        expenses_query = expenses_query.filter(models.Expense.date.between(start_date, end_date))
    
    expenses = expenses_query.all()
    expense_breakdown = {}
    for expense in expenses:
        category = expense.expense_category
        if category not in expense_breakdown:
            expense_breakdown[category] = 0
        expense_breakdown[category] += expense.amount
    
    return {
        **summary,
        "expense_breakdown": expense_breakdown
    }

def get_vendor_outstanding_balances(db: Session):
    """Get current outstanding balances for all vendors"""
    
    vendors = db.query(models.Vendor).all()
    balances = []
    
    for vendor in vendors:
        # Get latest ledger entry for running balance
        latest_entry = db.query(models.LedgerEntry).filter(
            models.LedgerEntry.vendor_id == vendor.id
        ).order_by(models.LedgerEntry.created_at.desc()).first()
        
        current_balance = latest_entry.running_balance if latest_entry else 0.0
        
        balances.append({
            "vendor_id": vendor.id,
            "vendor_name": vendor.name,
            "current_balance": current_balance,
            "contact_person": vendor.contact_person,
            "phone": vendor.phone
        })
    
    return balances

def get_vehicle_performance_report(db: Session, start_date: str = None, end_date: str = None):
    """Generate vehicle performance report"""
    
    vehicles = db.query(models.Vehicle).all()
    performance = []
    
    for vehicle in vehicles:
        # Get vehicle logs
        logs_query = db.query(models.VehicleLog).filter(models.VehicleLog.vehicle_id == vehicle.id)
        if start_date and end_date:
            logs_query = logs_query.filter(models.VehicleLog.date.between(start_date, end_date))
        
        logs = logs_query.all()
        
        # Get trips for this vehicle
        trips_query = db.query(models.Trip).filter(models.Trip.vehicle_id == vehicle.id)
        if start_date and end_date:
            trips_query = trips_query.filter(models.Trip.date.between(start_date, end_date))
        
        trips = trips_query.all()
        
        total_distance = sum(log.distance_covered for log in logs)
        total_fuel = sum(log.fuel_issued_quantity for log in logs)
        avg_efficiency = total_distance / total_fuel if total_fuel > 0 else 0
        
        total_revenue = sum(trip.net_amount for trip in trips)
        trip_count = len(trips)
        
        performance.append({
            "vehicle_id": vehicle.id,
            "vehicle_no": vehicle.vehicle_no,
            "vehicle_type": vehicle.vehicle_type,
            "total_distance": total_distance,
            "total_fuel": total_fuel,
            "avg_efficiency": avg_efficiency,
            "total_revenue": total_revenue,
            "trip_count": trip_count,
            "revenue_per_trip": total_revenue / trip_count if trip_count > 0 else 0
        })
    
    return performance
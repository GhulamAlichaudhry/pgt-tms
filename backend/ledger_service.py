"""
Ledger Service - Comprehensive ledger management for vendors and clients
Includes trip details, payment tracking, and filtering
"""

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from datetime import datetime, date
from typing import List, Optional, Dict, Any
import models

class LedgerService:
    """Service for managing financial ledgers"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_vendor_ledger(
        self,
        vendor_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_trips: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive vendor ledger with trip details and payments
        
        Returns:
            {
                "vendor": {...},
                "entries": [...],
                "summary": {
                    "total_debit": 0,
                    "total_credit": 0,
                    "balance": 0,
                    "trip_count": 0,
                    "payment_count": 0
                }
            }
        """
        vendor = self.db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()
        if not vendor:
            return None
        
        entries = []
        
        # Get all payables (trips) for this vendor
        payables_query = self.db.query(models.Payable).filter(
            models.Payable.vendor_id == vendor_id
        )
        
        if start_date:
            payables_query = payables_query.filter(models.Payable.date >= start_date)
        if end_date:
            payables_query = payables_query.filter(models.Payable.date <= end_date)
        
        payables = payables_query.options(
            joinedload(models.Payable.trip)
        ).order_by(models.Payable.date).all()
        
        # Get all payment requests for this vendor
        payments_query = self.db.query(models.PaymentRequest).filter(
            models.PaymentRequest.payable_id.in_([p.id for p in payables])
        )
        
        payments = payments_query.order_by(models.PaymentRequest.request_date).all()
        
        # Build ledger entries
        running_balance = 0
        
        for payable in payables:
            # Debit entry (we owe vendor)
            running_balance += payable.amount
            
            entry = {
                "id": f"payable_{payable.id}",
                "date": payable.date,
                "description": f"Trip: {payable.trip.reference_no if payable.trip else 'N/A'}",
                "trip_id": payable.trip_id,
                "trip_reference": payable.trip.reference_no if payable.trip else None,
                "trip_details": {
                    "from": payable.trip.source_location if payable.trip else None,
                    "to": payable.trip.destination_location if payable.trip else None,
                    "vehicle": payable.trip.vehicle_number if payable.trip else None,
                    "tonnage": payable.trip.total_tonnage if payable.trip else None,
                } if include_trips and payable.trip else None,
                "debit": float(payable.amount),
                "credit": 0,
                "balance": running_balance,
                "type": "trip",
                "status": "paid" if payable.outstanding_amount == 0 else ("partial" if payable.outstanding_amount < payable.amount else "pending"),
                "outstanding": float(payable.outstanding_amount) if payable.outstanding_amount else float(payable.amount)
            }
            entries.append(entry)
        
        # Add payment entries
        for payment in payments:
            if payment.status == "approved":
                running_balance -= payment.amount_paid
                
                payable = next((p for p in payables if p.id == payment.payable_id), None)
                
                entry = {
                    "id": f"payment_{payment.id}",
                    "date": payment.payment_date or payment.request_date,
                    "description": f"Payment: {payment.payment_method}",
                    "trip_id": payable.trip_id if payable else None,
                    "trip_reference": payable.trip.reference_no if payable and payable.trip else None,
                    "payment_id": payment.id,
                    "debit": 0,
                    "credit": float(payment.amount_paid),
                    "balance": running_balance,
                    "type": "payment",
                    "status": "paid",
                    "payment_method": payment.payment_method,
                    "payment_reference": payment.payment_reference
                }
                entries.append(entry)
        
        # Sort all entries by date
        entries.sort(key=lambda x: x["date"])
        
        # Recalculate running balance
        running_balance = 0
        for entry in entries:
            running_balance += entry["debit"] - entry["credit"]
            entry["balance"] = running_balance
        
        # Calculate summary
        total_debit = sum(e["debit"] for e in entries)
        total_credit = sum(e["credit"] for e in entries)
        trip_count = len([e for e in entries if e["type"] == "trip"])
        payment_count = len([e for e in entries if e["type"] == "payment"])
        
        return {
            "vendor": {
                "id": vendor.id,
                "name": vendor.name,
                "code": vendor.vendor_code,
                "contact": vendor.contact_person,
                "phone": vendor.phone
            },
            "entries": entries,
            "summary": {
                "total_debit": total_debit,
                "total_credit": total_credit,
                "balance": total_debit - total_credit,
                "trip_count": trip_count,
                "payment_count": payment_count
            }
        }
    
    def get_client_ledger(
        self,
        client_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        include_trips: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive client ledger with trip details and payments
        
        Returns:
            {
                "client": {...},
                "entries": [...],
                "summary": {
                    "total_debit": 0,
                    "total_credit": 0,
                    "balance": 0,
                    "trip_count": 0,
                    "payment_count": 0
                }
            }
        """
        client = self.db.query(models.Client).filter(models.Client.id == client_id).first()
        if not client:
            return None
        
        entries = []
        
        # Get all receivables (trips) for this client
        receivables_query = self.db.query(models.Receivable).filter(
            models.Receivable.client_id == client_id
        )
        
        if start_date:
            receivables_query = receivables_query.filter(models.Receivable.invoice_date >= start_date)
        if end_date:
            receivables_query = receivables_query.filter(models.Receivable.invoice_date <= end_date)
        
        receivables = receivables_query.options(
            joinedload(models.Receivable.trip)
        ).order_by(models.Receivable.invoice_date).all()
        
        # Build ledger entries
        running_balance = 0
        
        for receivable in receivables:
            # Debit entry (client owes us)
            running_balance += receivable.amount
            
            entry = {
                "id": f"receivable_{receivable.id}",
                "date": receivable.invoice_date,
                "description": f"Trip: {receivable.trip.reference_no if receivable.trip else 'N/A'}",
                "trip_id": receivable.trip_id,
                "trip_reference": receivable.trip.reference_no if receivable.trip else None,
                "trip_details": {
                    "from": receivable.trip.source_location if receivable.trip else None,
                    "to": receivable.trip.destination_location if receivable.trip else None,
                    "vehicle": receivable.trip.vehicle_number if receivable.trip else None,
                    "tonnage": receivable.trip.total_tonnage if receivable.trip else None,
                } if include_trips and receivable.trip else None,
                "debit": float(receivable.amount),
                "credit": float(receivable.amount_paid) if receivable.amount_paid else 0,
                "balance": running_balance,
                "type": "trip",
                "status": "paid" if receivable.remaining_amount == 0 else ("partial" if receivable.amount_paid > 0 else "pending"),
                "outstanding": float(receivable.remaining_amount) if receivable.remaining_amount else float(receivable.amount)
            }
            
            # If there's a payment, adjust balance
            if receivable.amount_paid and receivable.amount_paid > 0:
                running_balance -= receivable.amount_paid
                entry["balance"] = running_balance
            
            entries.append(entry)
        
        # Calculate summary
        total_debit = sum(e["debit"] for e in entries)
        total_credit = sum(e["credit"] for e in entries)
        trip_count = len([e for e in entries if e["type"] == "trip"])
        payment_count = len([e for e in entries if e["credit"] > 0])
        
        return {
            "client": {
                "id": client.id,
                "name": client.name,
                "code": client.client_code,
                "contact": client.contact_person,
                "phone": client.phone
            },
            "entries": entries,
            "summary": {
                "total_debit": total_debit,
                "total_credit": total_credit,
                "balance": total_debit - total_credit,
                "trip_count": trip_count,
                "payment_count": payment_count
            }
        }
    
    def get_all_vendors_summary(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get summary of all vendors with outstanding balances"""
        vendors = self.db.query(models.Vendor).filter(models.Vendor.is_active == True).all()
        
        summary = []
        for vendor in vendors:
            ledger = self.get_vendor_ledger(vendor.id, start_date, end_date, include_trips=False)
            if ledger:
                summary.append({
                    "vendor_id": vendor.id,
                    "vendor_name": vendor.name,
                    "vendor_code": vendor.vendor_code,
                    "total_debit": ledger["summary"]["total_debit"],
                    "total_credit": ledger["summary"]["total_credit"],
                    "balance": ledger["summary"]["balance"],
                    "trip_count": ledger["summary"]["trip_count"],
                    "payment_count": ledger["summary"]["payment_count"]
                })
        
        return summary
    
    def get_all_clients_summary(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Get summary of all clients with outstanding balances"""
        clients = self.db.query(models.Client).filter(models.Client.is_active == True).all()
        
        summary = []
        for client in clients:
            ledger = self.get_client_ledger(client.id, start_date, end_date, include_trips=False)
            if ledger:
                summary.append({
                    "client_id": client.id,
                    "client_name": client.name,
                    "client_code": client.client_code,
                    "total_debit": ledger["summary"]["total_debit"],
                    "total_credit": ledger["summary"]["total_credit"],
                    "balance": ledger["summary"]["balance"],
                    "trip_count": ledger["summary"]["trip_count"],
                    "payment_count": ledger["summary"]["payment_count"]
                })
        
        return summary

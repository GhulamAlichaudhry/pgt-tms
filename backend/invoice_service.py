"""
Invoice Service
Manages invoice generation, storage, and operations
"""
from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from pathlib import Path
import os
import models
from enhanced_invoice_generator import enhanced_invoice_generator
from modern_invoice_generator import modern_invoice_generator, modern_invoice_generator_blue, modern_invoice_generator_red
from email_service import email_service

class InvoiceService:
    def __init__(self, db: Session, use_modern=True, theme='red_black'):
        self.db = db
        self.use_modern = use_modern
        self.theme = theme
        
        # Select generator based on preference
        if use_modern:
            if theme == 'blue':
                self.generator = modern_invoice_generator_blue
            else:
                self.generator = modern_invoice_generator_red
        else:
            self.generator = enhanced_invoice_generator
            
        self.invoice_storage_path = Path("invoices")
        self.invoice_storage_path.mkdir(exist_ok=True)
    
    def generate_invoice_from_trip(
        self,
        trip_id: int,
        auto_email: bool = False,
        store_pdf: bool = True
    ) -> Dict:
        """
        Generate invoice from trip
        
        Returns:
            {
                'success': True,
                'invoice_id': 123,
                'invoice_number': 'INV-2026-001',
                'pdf_path': 'invoices/INV-2026-001.pdf',
                'emailed': False
            }
        """
        try:
            # Get trip
            trip = self.db.query(models.Trip).filter(models.Trip.id == trip_id).first()
            if not trip:
                return {'success': False, 'error': 'Trip not found'}
            
            # Check if receivable exists
            receivable = self.db.query(models.Receivable).filter(
                models.Receivable.trip_id == trip_id
            ).first()
            
            if not receivable:
                return {'success': False, 'error': 'No receivable found for this trip'}
            
            # Generate PDF
            pdf_buffer = self.generator.generate_invoice_from_trip_id(self.db, trip_id)
            
            # Store PDF if requested
            pdf_path = None
            if store_pdf:
                pdf_filename = f"{receivable.invoice_number}.pdf"
                pdf_path = self.invoice_storage_path / pdf_filename
                
                with open(pdf_path, 'wb') as f:
                    f.write(pdf_buffer.getvalue())
                
                # Update receivable with PDF path
                receivable.invoice_pdf_path = str(pdf_path)
                receivable.invoice_generated_at = datetime.now()
                self.db.commit()
            
            # Email if requested
            emailed = False
            if auto_email and trip.client.email:
                email_result = self.email_invoice(receivable.id)
                emailed = email_result.get('success', False)
            
            return {
                'success': True,
                'invoice_id': receivable.id,
                'invoice_number': receivable.invoice_number,
                'pdf_path': str(pdf_path) if pdf_path else None,
                'emailed': emailed
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def regenerate_invoice(self, receivable_id: int) -> Dict:
        """Regenerate invoice PDF for existing receivable"""
        try:
            receivable = self.db.query(models.Receivable).filter(
                models.Receivable.id == receivable_id
            ).first()
            
            if not receivable:
                return {'success': False, 'error': 'Receivable not found'}
            
            if not receivable.trip_id:
                return {'success': False, 'error': 'No trip associated with this receivable'}
            
            # Generate new PDF
            pdf_buffer = self.generator.generate_invoice_from_trip_id(self.db, receivable.trip_id)
            
            # Store PDF
            pdf_filename = f"{receivable.invoice_number}.pdf"
            pdf_path = self.invoice_storage_path / pdf_filename
            
            with open(pdf_path, 'wb') as f:
                f.write(pdf_buffer.getvalue())
            
            # Update receivable
            receivable.invoice_pdf_path = str(pdf_path)
            receivable.invoice_generated_at = datetime.now()
            self.db.commit()
            
            return {
                'success': True,
                'invoice_id': receivable.id,
                'invoice_number': receivable.invoice_number,
                'pdf_path': str(pdf_path)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_invoice_pdf(self, receivable_id: int):
        """Get stored invoice PDF"""
        receivable = self.db.query(models.Receivable).filter(
            models.Receivable.id == receivable_id
        ).first()
        
        if not receivable:
            return None
        
        # If PDF exists, return it
        if receivable.invoice_pdf_path and os.path.exists(receivable.invoice_pdf_path):
            with open(receivable.invoice_pdf_path, 'rb') as f:
                return f.read()
        
        # If no PDF stored, generate on-the-fly
        if receivable.trip_id:
            pdf_buffer = self.generator.generate_invoice_from_trip_id(self.db, receivable.trip_id)
            return pdf_buffer.getvalue()
        
        return None
    
    def email_invoice(self, receivable_id: int) -> Dict:
        """Email invoice to client"""
        try:
            receivable = self.db.query(models.Receivable).filter(
                models.Receivable.id == receivable_id
            ).first()
            
            if not receivable:
                return {'success': False, 'error': 'Receivable not found'}
            
            if not receivable.client.email:
                return {'success': False, 'error': 'Client email not found'}
            
            # Get or generate PDF
            pdf_data = self.get_invoice_pdf(receivable_id)
            if not pdf_data:
                return {'success': False, 'error': 'Could not generate invoice PDF'}
            
            # Send email
            result = email_service.send_invoice_email(
                to_email=receivable.client.email,
                client_name=receivable.client.name,
                invoice_number=receivable.invoice_number,
                amount=receivable.total_amount,
                pdf_attachment=pdf_data
            )
            
            if result['success']:
                # Update sent timestamp
                receivable.invoice_sent_at = datetime.now()
                self.db.commit()
            
            return result
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def bulk_generate_invoices(
        self,
        trip_ids: List[int],
        auto_email: bool = False
    ) -> Dict:
        """Generate invoices for multiple trips"""
        results = {
            'success': True,
            'generated': 0,
            'failed': 0,
            'emailed': 0,
            'details': []
        }
        
        for trip_id in trip_ids:
            result = self.generate_invoice_from_trip(trip_id, auto_email=auto_email)
            
            if result['success']:
                results['generated'] += 1
                if result.get('emailed'):
                    results['emailed'] += 1
            else:
                results['failed'] += 1
            
            results['details'].append({
                'trip_id': trip_id,
                'result': result
            })
        
        return results
    
    def get_invoice_summary(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        client_id: Optional[int] = None
    ) -> Dict:
        """Get invoice summary statistics"""
        query = self.db.query(models.Receivable)
        
        if start_date:
            query = query.filter(models.Receivable.invoice_date >= start_date)
        if end_date:
            query = query.filter(models.Receivable.invoice_date <= end_date)
        if client_id:
            query = query.filter(models.Receivable.client_id == client_id)
        
        receivables = query.all()
        
        total_invoices = len(receivables)
        total_amount = sum(r.total_amount for r in receivables)
        paid_amount = sum(r.paid_amount for r in receivables)
        outstanding_amount = sum(r.remaining_amount for r in receivables)
        
        # Status breakdown
        status_counts = {}
        for r in receivables:
            status = r.status.value if hasattr(r.status, 'value') else str(r.status)
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Invoices with PDFs
        invoices_with_pdf = sum(1 for r in receivables if r.invoice_pdf_path)
        invoices_emailed = sum(1 for r in receivables if r.invoice_sent_at)
        
        return {
            'total_invoices': total_invoices,
            'total_amount': float(total_amount),
            'paid_amount': float(paid_amount),
            'outstanding_amount': float(outstanding_amount),
            'status_breakdown': status_counts,
            'invoices_with_pdf': invoices_with_pdf,
            'invoices_emailed': invoices_emailed,
            'collection_rate': (paid_amount / total_amount * 100) if total_amount > 0 else 0
        }
    
    def list_invoices(
        self,
        client_id: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Dict]:
        """List invoices with filters"""
        query = self.db.query(models.Receivable)
        
        if client_id:
            query = query.filter(models.Receivable.client_id == client_id)
        if status:
            query = query.filter(models.Receivable.status == status)
        if start_date:
            query = query.filter(models.Receivable.invoice_date >= start_date)
        if end_date:
            query = query.filter(models.Receivable.invoice_date <= end_date)
        
        receivables = query.order_by(models.Receivable.invoice_date.desc()).offset(skip).limit(limit).all()
        
        return [
            {
                'id': r.id,
                'invoice_number': r.invoice_number,
                'client_name': r.client.name if r.client else 'Unknown',
                'invoice_date': r.invoice_date.isoformat(),
                'due_date': r.due_date.isoformat(),
                'total_amount': float(r.total_amount),
                'paid_amount': float(r.paid_amount),
                'remaining_amount': float(r.remaining_amount),
                'status': r.status.value if hasattr(r.status, 'value') else str(r.status),
                'has_pdf': bool(r.invoice_pdf_path),
                'emailed': bool(r.invoice_sent_at),
                'trip_reference': r.trip.reference_no if r.trip else None
            }
            for r in receivables
        ]

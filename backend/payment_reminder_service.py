"""
Automated Payment Reminder Service
Sends reminders for overdue and upcoming payments
"""
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Dict
import models
from email_service import email_service

class PaymentReminderService:
    def __init__(self, db: Session):
        self.db = db
        
        # Reminder rules (days relative to due date)
        self.reminder_rules = {
            'before_due': -7,      # 7 days before due date
            'on_due': 0,           # On due date
            'after_3_days': 3,     # 3 days after due date
            'after_7_days': 7,     # 7 days after due date
            'after_14_days': 14,   # 14 days after due date
            'after_30_days': 30    # 30 days after due date
        }
    
    def get_receivables_needing_reminder(self) -> List[models.Receivable]:
        """Get all receivables that need reminders"""
        today = date.today()
        receivables_to_remind = []
        
        # Get all unpaid receivables
        receivables = self.db.query(models.Receivable).filter(
            models.Receivable.remaining_amount > 0,
            models.Receivable.status != 'cancelled'
        ).all()
        
        for receivable in receivables:
            due_date = receivable.due_date.date() if hasattr(receivable.due_date, 'date') else receivable.due_date
            days_diff = (today - due_date).days
            
            # Check if reminder should be sent
            should_remind = False
            reminder_type = None
            
            for rule_name, rule_days in self.reminder_rules.items():
                if days_diff == rule_days:
                    should_remind = True
                    reminder_type = rule_name
                    break
            
            if should_remind:
                receivables_to_remind.append({
                    'receivable': receivable,
                    'reminder_type': reminder_type,
                    'days_diff': days_diff
                })
        
        return receivables_to_remind
    
    def send_reminder(self, receivable: models.Receivable, reminder_type: str, days_diff: int) -> Dict:
        """Send payment reminder email"""
        if not receivable.client.email:
            return {
                "success": False,
                "error": "Client email not found"
            }
        
        # Calculate days overdue
        days_overdue = max(0, days_diff)
        
        # Send email
        result = email_service.send_payment_reminder(
            to_email=receivable.client.email,
            client_name=receivable.client.name,
            invoice_number=receivable.invoice_number,
            amount=receivable.remaining_amount,
            due_date=receivable.due_date.strftime('%Y-%m-%d'),
            days_overdue=days_overdue
        )
        
        # Log reminder
        if result["success"]:
            self._log_reminder(receivable.id, reminder_type, days_diff)
        
        return result
    
    def send_all_reminders(self) -> Dict:
        """Send all pending reminders"""
        receivables_to_remind = self.get_receivables_needing_reminder()
        
        results = {
            'total': len(receivables_to_remind),
            'sent': 0,
            'failed': 0,
            'details': []
        }
        
        for item in receivables_to_remind:
            receivable = item['receivable']
            reminder_type = item['reminder_type']
            days_diff = item['days_diff']
            
            result = self.send_reminder(receivable, reminder_type, days_diff)
            
            if result["success"]:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            results['details'].append({
                'invoice_number': receivable.invoice_number,
                'client_name': receivable.client.name,
                'reminder_type': reminder_type,
                'success': result["success"],
                'error': result.get("error")
            })
        
        return results
    
    def send_manual_reminder(self, receivable_id: int) -> Dict:
        """Send manual reminder for specific receivable"""
        receivable = self.db.query(models.Receivable).filter(
            models.Receivable.id == receivable_id
        ).first()
        
        if not receivable:
            return {
                "success": False,
                "error": "Receivable not found"
            }
        
        due_date = receivable.due_date.date() if hasattr(receivable.due_date, 'date') else receivable.due_date
        days_diff = (date.today() - due_date).days
        
        return self.send_reminder(receivable, 'manual', days_diff)
    
    def _log_reminder(self, receivable_id: int, reminder_type: str, days_diff: int):
        """Log reminder in system settings"""
        log_entry = {
            'receivable_id': receivable_id,
            'reminder_type': reminder_type,
            'days_diff': days_diff,
            'sent_at': datetime.now().isoformat()
        }
        
        # Store in system settings (you might want to create a ReminderLog model)
        setting = models.SystemSetting(
            setting_key=f"reminder_log_{receivable_id}_{datetime.now().timestamp()}",
            setting_value=str(log_entry),
            setting_type="json",
            description=f"Payment reminder log for receivable {receivable_id}",
            is_public=False
        )
        self.db.add(setting)
        self.db.commit()
    
    def get_reminder_history(self, receivable_id: int) -> List[Dict]:
        """Get reminder history for receivable"""
        settings = self.db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key.like(f"reminder_log_{receivable_id}_%")
        ).all()
        
        history = []
        for setting in settings:
            try:
                import ast
                log_entry = ast.literal_eval(setting.setting_value)
                history.append(log_entry)
            except:
                continue
        
        return sorted(history, key=lambda x: x['sent_at'], reverse=True)
    
    def get_overdue_summary(self) -> Dict:
        """Get summary of overdue receivables"""
        today = date.today()
        
        # Get all overdue receivables
        overdue_receivables = self.db.query(models.Receivable).filter(
            models.Receivable.remaining_amount > 0,
            models.Receivable.due_date < datetime.now(),
            models.Receivable.status != 'cancelled'
        ).all()
        
        # Categorize by age
        summary = {
            '1-7_days': {'count': 0, 'amount': 0, 'receivables': []},
            '8-14_days': {'count': 0, 'amount': 0, 'receivables': []},
            '15-30_days': {'count': 0, 'amount': 0, 'receivables': []},
            '30+_days': {'count': 0, 'amount': 0, 'receivables': []},
            'total': {'count': 0, 'amount': 0}
        }
        
        for receivable in overdue_receivables:
            due_date = receivable.due_date.date() if hasattr(receivable.due_date, 'date') else receivable.due_date
            days_overdue = (today - due_date).days
            
            receivable_info = {
                'id': receivable.id,
                'invoice_number': receivable.invoice_number,
                'client_name': receivable.client.name,
                'amount': receivable.remaining_amount,
                'days_overdue': days_overdue
            }
            
            if days_overdue <= 7:
                category = '1-7_days'
            elif days_overdue <= 14:
                category = '8-14_days'
            elif days_overdue <= 30:
                category = '15-30_days'
            else:
                category = '30+_days'
            
            summary[category]['count'] += 1
            summary[category]['amount'] += receivable.remaining_amount
            summary[category]['receivables'].append(receivable_info)
            
            summary['total']['count'] += 1
            summary['total']['amount'] += receivable.remaining_amount
        
        return summary

# Scheduled reminder function
def send_daily_reminders(db: Session):
    """Run daily to send all pending reminders"""
    service = PaymentReminderService(db)
    results = service.send_all_reminders()
    
    print(f"✅ Payment reminders sent: {results['sent']} successful, {results['failed']} failed")
    return results

if __name__ == "__main__":
    # Test reminder service
    from database import SessionLocal
    db = SessionLocal()
    try:
        send_daily_reminders(db)
    finally:
        db.close()

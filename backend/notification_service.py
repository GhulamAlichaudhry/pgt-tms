"""
Notification Service
Handles in-app notifications and alerts
"""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import models

class NotificationService:
    """Service for managing user notifications"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_notification(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "info",
        link: Optional[str] = None
    ) -> models.Notification:
        """
        Create a new notification for a user
        
        Args:
            user_id: ID of user to notify
            title: Notification title
            message: Notification message
            notification_type: Type (info, warning, error, success)
            link: Optional URL to navigate to
        
        Returns:
            Created Notification object
        """
        notification = models.Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            link=link
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        
        return notification
    
    def get_user_notifications(
        self,
        user_id: int,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[models.Notification]:
        """Get notifications for a user"""
        query = self.db.query(models.Notification).filter(
            models.Notification.user_id == user_id
        )
        
        if unread_only:
            query = query.filter(models.Notification.is_read == False)
        
        return query.order_by(
            models.Notification.created_at.desc()
        ).limit(limit).all()
    
    def mark_as_read(self, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read"""
        notification = self.db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        ).first()
        
        if notification:
            notification.is_read = True
            notification.read_at = datetime.now()
            self.db.commit()
            return True
        
        return False
    
    def mark_all_as_read(self, user_id: int) -> int:
        """Mark all notifications as read for a user"""
        count = self.db.query(models.Notification).filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == False
        ).update({
            "is_read": True,
            "read_at": datetime.now()
        })
        
        self.db.commit()
        return count
    
    def get_unread_count(self, user_id: int) -> int:
        """Get count of unread notifications"""
        return self.db.query(models.Notification).filter(
            models.Notification.user_id == user_id,
            models.Notification.is_read == False
        ).count()
    
    def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """Delete a notification"""
        notification = self.db.query(models.Notification).filter(
            models.Notification.id == notification_id,
            models.Notification.user_id == user_id
        ).first()
        
        if notification:
            self.db.delete(notification)
            self.db.commit()
            return True
        
        return False
    
    def delete_old_notifications(self, days: int = 90) -> int:
        """Delete notifications older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        count = self.db.query(models.Notification).filter(
            models.Notification.created_at < cutoff_date,
            models.Notification.is_read == True
        ).delete()
        
        self.db.commit()
        return count
    
    # Predefined notification creators
    def notify_payment_request_submitted(
        self,
        admin_user_ids: List[int],
        vendor_name: str,
        amount: float,
        payment_request_id: int
    ):
        """Notify admins of new payment request"""
        for user_id in admin_user_ids:
            self.create_notification(
                user_id=user_id,
                title="New Payment Request",
                message=f"Payment request from {vendor_name} for PKR {amount:,.2f}",
                notification_type="info",
                link=f"/payables?highlight={payment_request_id}"
            )
    
    def notify_payment_approved(
        self,
        requester_id: int,
        vendor_name: str,
        amount: float
    ):
        """Notify requester that payment was approved"""
        self.create_notification(
            user_id=requester_id,
            title="Payment Approved",
            message=f"Payment to {vendor_name} for PKR {amount:,.2f} has been approved",
            notification_type="success",
            link="/payables"
        )
    
    def notify_payment_rejected(
        self,
        requester_id: int,
        vendor_name: str,
        amount: float,
        reason: str
    ):
        """Notify requester that payment was rejected"""
        self.create_notification(
            user_id=requester_id,
            title="Payment Rejected",
            message=f"Payment to {vendor_name} for PKR {amount:,.2f} was rejected: {reason}",
            notification_type="warning",
            link="/payables"
        )
    
    def notify_invoice_due_soon(
        self,
        user_id: int,
        client_name: str,
        invoice_number: str,
        amount: float,
        due_date: datetime
    ):
        """Notify about upcoming invoice due date"""
        days_until_due = (due_date - datetime.now()).days
        
        self.create_notification(
            user_id=user_id,
            title="Invoice Due Soon",
            message=f"Invoice {invoice_number} from {client_name} (PKR {amount:,.2f}) due in {days_until_due} days",
            notification_type="warning",
            link="/receivables"
        )
    
    def notify_invoice_overdue(
        self,
        user_id: int,
        client_name: str,
        invoice_number: str,
        amount: float,
        days_overdue: int
    ):
        """Notify about overdue invoice"""
        self.create_notification(
            user_id=user_id,
            title="Invoice Overdue",
            message=f"Invoice {invoice_number} from {client_name} (PKR {amount:,.2f}) is {days_overdue} days overdue",
            notification_type="error",
            link="/receivables"
        )
    
    def notify_low_cash_balance(
        self,
        admin_user_ids: List[int],
        current_balance: float,
        threshold: float
    ):
        """Notify admins of low cash balance"""
        for user_id in admin_user_ids:
            self.create_notification(
                user_id=user_id,
                title="Low Cash Balance Alert",
                message=f"Cash balance (PKR {current_balance:,.2f}) is below threshold (PKR {threshold:,.2f})",
                notification_type="warning",
                link="/dashboard"
            )
    
    def notify_trip_created(
        self,
        user_id: int,
        trip_reference: str,
        client_name: str,
        amount: float
    ):
        """Notify about new trip creation"""
        self.create_notification(
            user_id=user_id,
            title="New Trip Created",
            message=f"Trip {trip_reference} for {client_name} (PKR {amount:,.2f}) has been created",
            notification_type="success",
            link="/fleet-logs"
        )

def get_admin_user_ids(db: Session) -> List[int]:
    """Get all admin user IDs for notifications"""
    admins = db.query(models.User).filter(
        models.User.role == models.UserRole.ADMIN,
        models.User.is_active == True
    ).all()
    
    return [admin.id for admin in admins]

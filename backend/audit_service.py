"""
Audit Trail Service
Tracks all user actions and data changes for compliance and security
"""

from sqlalchemy.orm import Session
from datetime import datetime
import json
from typing import Optional, Dict, Any
import models

class AuditService:
    """Service for logging user actions and data changes"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def log_action(
        self,
        user_id: int,
        action: str,
        table_name: str,
        record_id: Optional[int] = None,
        old_values: Optional[Dict[str, Any]] = None,
        new_values: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        description: Optional[str] = None
    ) -> models.AuditLog:
        """
        Log an audit trail entry
        
        Args:
            user_id: ID of user performing action
            action: Type of action (create, update, delete, login, logout, etc.)
            table_name: Name of table affected
            record_id: ID of record affected (if applicable)
            old_values: Previous values (for updates/deletes)
            new_values: New values (for creates/updates)
            ip_address: User's IP address
            user_agent: User's browser/client info
            description: Human-readable description
        
        Returns:
            Created AuditLog entry
        """
        audit_log = models.AuditLog(
            user_id=user_id,
            action=action,
            table_name=table_name,
            record_id=record_id,
            old_values=json.dumps(old_values) if old_values else None,
            new_values=json.dumps(new_values) if new_values else None,
            ip_address=ip_address,
            user_agent=user_agent,
            description=description
        )
        
        self.db.add(audit_log)
        self.db.commit()
        self.db.refresh(audit_log)
        
        return audit_log
    
    def log_create(
        self,
        user_id: int,
        table_name: str,
        record_id: int,
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> models.AuditLog:
        """Log a record creation"""
        return self.log_action(
            user_id=user_id,
            action="create",
            table_name=table_name,
            record_id=record_id,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            description=f"Created {table_name} record #{record_id}"
        )
    
    def log_update(
        self,
        user_id: int,
        table_name: str,
        record_id: int,
        old_values: Dict[str, Any],
        new_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> models.AuditLog:
        """Log a record update"""
        # Only log changed fields
        changes = {}
        for key in new_values:
            if key in old_values and old_values[key] != new_values[key]:
                changes[key] = {"old": old_values[key], "new": new_values[key]}
        
        return self.log_action(
            user_id=user_id,
            action="update",
            table_name=table_name,
            record_id=record_id,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            description=f"Updated {table_name} record #{record_id}: {', '.join(changes.keys())}"
        )
    
    def log_delete(
        self,
        user_id: int,
        table_name: str,
        record_id: int,
        old_values: Dict[str, Any],
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> models.AuditLog:
        """Log a record deletion"""
        return self.log_action(
            user_id=user_id,
            action="delete",
            table_name=table_name,
            record_id=record_id,
            old_values=old_values,
            ip_address=ip_address,
            user_agent=user_agent,
            description=f"Deleted {table_name} record #{record_id}"
        )
    
    def log_login(
        self,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True
    ) -> models.AuditLog:
        """Log a user login attempt"""
        return self.log_action(
            user_id=user_id,
            action="login_success" if success else "login_failed",
            table_name="users",
            record_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            description=f"User login {'successful' if success else 'failed'}"
        )
    
    def log_logout(
        self,
        user_id: int,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> models.AuditLog:
        """Log a user logout"""
        return self.log_action(
            user_id=user_id,
            action="logout",
            table_name="users",
            record_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            description="User logged out"
        )
    
    def get_audit_trail(
        self,
        table_name: Optional[str] = None,
        record_id: Optional[int] = None,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ):
        """
        Query audit trail with filters
        
        Returns list of audit log entries matching criteria
        """
        query = self.db.query(models.AuditLog)
        
        if table_name:
            query = query.filter(models.AuditLog.table_name == table_name)
        if record_id:
            query = query.filter(models.AuditLog.record_id == record_id)
        if user_id:
            query = query.filter(models.AuditLog.user_id == user_id)
        if action:
            query = query.filter(models.AuditLog.action == action)
        if start_date:
            query = query.filter(models.AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(models.AuditLog.timestamp <= end_date)
        
        query = query.order_by(models.AuditLog.timestamp.desc())
        query = query.offset(offset).limit(limit)
        
        return query.all()
    
    def get_record_history(
        self,
        table_name: str,
        record_id: int
    ):
        """Get complete history of changes for a specific record"""
        return self.db.query(models.AuditLog).filter(
            models.AuditLog.table_name == table_name,
            models.AuditLog.record_id == record_id
        ).order_by(models.AuditLog.timestamp.asc()).all()
    
    def get_user_activity(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ):
        """Get all activity for a specific user"""
        query = self.db.query(models.AuditLog).filter(
            models.AuditLog.user_id == user_id
        )
        
        if start_date:
            query = query.filter(models.AuditLog.timestamp >= start_date)
        if end_date:
            query = query.filter(models.AuditLog.timestamp <= end_date)
        
        return query.order_by(models.AuditLog.timestamp.desc()).limit(limit).all()

def get_client_ip(request) -> Optional[str]:
    """Extract client IP address from request"""
    # Check for forwarded IP (behind proxy)
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    
    # Check for real IP
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct client
    if hasattr(request, "client") and request.client:
        return request.client.host
    
    return None

def get_user_agent(request) -> Optional[str]:
    """Extract user agent from request"""
    return request.headers.get("User-Agent")

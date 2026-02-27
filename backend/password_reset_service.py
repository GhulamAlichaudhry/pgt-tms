"""
Password Reset Service
Handles password reset tokens and validation
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
import models
import auth
from email_service import email_service

class PasswordResetService:
    TOKEN_EXPIRY_HOURS = 1
    
    @staticmethod
    def generate_reset_token() -> str:
        """Generate a secure random token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_reset_token(db: Session, email: str) -> dict:
        """Create a password reset token for user"""
        # Find user by email
        user = db.query(models.User).filter(models.User.email == email).first()
        
        if not user:
            # Don't reveal if email exists
            return {
                "success": True,
                "message": "If the email exists, a reset link has been sent"
            }
        
        # Generate token
        token = PasswordResetService.generate_reset_token()
        expires_at = datetime.now() + timedelta(hours=PasswordResetService.TOKEN_EXPIRY_HOURS)
        
        # Store token (you might want to create a PasswordResetToken model)
        # For now, we'll use a simple approach with system settings
        reset_data = {
            "token": token,
            "user_id": user.id,
            "expires_at": expires_at.isoformat(),
            "used": False
        }
        
        # Store in system settings (temporary solution)
        setting_key = f"password_reset_{token}"
        setting = models.SystemSetting(
            setting_key=setting_key,
            setting_value=str(reset_data),
            setting_type="json",
            description=f"Password reset token for user {user.id}",
            is_public=False
        )
        db.add(setting)
        db.commit()
        
        # Send email
        email_result = email_service.send_password_reset_email(
            to_email=user.email,
            reset_token=token,
            username=user.username
        )
        
        if email_result["success"]:
            return {
                "success": True,
                "message": "Password reset email sent successfully"
            }
        else:
            return {
                "success": False,
                "error": "Failed to send email"
            }
    
    @staticmethod
    def validate_reset_token(db: Session, token: str) -> Optional[models.User]:
        """Validate reset token and return user"""
        setting_key = f"password_reset_{token}"
        setting = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key == setting_key
        ).first()
        
        if not setting:
            return None
        
        # Parse token data
        import ast
        try:
            reset_data = ast.literal_eval(setting.setting_value)
        except:
            return None
        
        # Check if token is expired
        expires_at = datetime.fromisoformat(reset_data["expires_at"])
        if datetime.now() > expires_at:
            return None
        
        # Check if token is already used
        if reset_data.get("used", False):
            return None
        
        # Get user
        user = db.query(models.User).filter(
            models.User.id == reset_data["user_id"]
        ).first()
        
        return user
    
    @staticmethod
    def reset_password(db: Session, token: str, new_password: str) -> dict:
        """Reset user password using token"""
        user = PasswordResetService.validate_reset_token(db, token)
        
        if not user:
            return {
                "success": False,
                "error": "Invalid or expired token"
            }
        
        # Update password
        user.hashed_password = auth.get_password_hash(new_password)
        
        # Mark token as used
        setting_key = f"password_reset_{token}"
        setting = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key == setting_key
        ).first()
        
        if setting:
            import ast
            reset_data = ast.literal_eval(setting.setting_value)
            reset_data["used"] = True
            setting.setting_value = str(reset_data)
        
        db.commit()
        
        return {
            "success": True,
            "message": "Password reset successfully"
        }
    
    @staticmethod
    def cleanup_expired_tokens(db: Session):
        """Remove expired reset tokens"""
        # Get all password reset settings
        settings = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key.like("password_reset_%")
        ).all()
        
        for setting in settings:
            try:
                import ast
                reset_data = ast.literal_eval(setting.setting_value)
                expires_at = datetime.fromisoformat(reset_data["expires_at"])
                
                # Delete if expired or used
                if datetime.now() > expires_at or reset_data.get("used", False):
                    db.delete(setting)
            except:
                # Delete corrupted settings
                db.delete(setting)
        
        db.commit()

"""
Two-Factor Authentication Service
Implements OTP-based 2FA for enhanced security
"""
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Dict
from sqlalchemy.orm import Session
import models
from email_service import email_service

class TwoFactorAuthService:
    OTP_LENGTH = 6
    OTP_EXPIRY_MINUTES = 10
    
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP"""
        return ''.join(secrets.choice(string.digits) for _ in range(TwoFactorAuthService.OTP_LENGTH))
    
    @staticmethod
    def send_otp(db: Session, user_id: int) -> Dict:
        """Generate and send OTP to user"""
        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        if not user:
            return {"success": False, "error": "User not found"}
        
        if not user.email:
            return {"success": False, "error": "User email not found"}
        
        # Generate OTP
        otp = TwoFactorAuthService.generate_otp()
        expires_at = datetime.now() + timedelta(minutes=TwoFactorAuthService.OTP_EXPIRY_MINUTES)
        
        # Store OTP
        otp_data = {
            "otp": otp,
            "user_id": user_id,
            "expires_at": expires_at.isoformat(),
            "used": False
        }
        
        setting_key = f"2fa_otp_{user_id}_{datetime.now().timestamp()}"
        setting = models.SystemSetting(
            setting_key=setting_key,
            setting_value=str(otp_data),
            setting_type="json",
            description=f"2FA OTP for user {user_id}",
            is_public=False
        )
        db.add(setting)
        db.commit()
        
        # Send email
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9fafb; padding: 30px; }}
                .otp-box {{ 
                    background: white; 
                    border: 3px solid #dc2626; 
                    padding: 20px; 
                    margin: 20px 0;
                    text-align: center;
                    border-radius: 8px;
                }}
                .otp-code {{ 
                    font-size: 36px; 
                    font-weight: bold; 
                    color: #dc2626;
                    letter-spacing: 8px;
                }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>PGT International TMS</h1>
                    <p>Two-Factor Authentication</p>
                </div>
                <div class="content">
                    <p>Hello {user.full_name},</p>
                    <p>Your verification code is:</p>
                    
                    <div class="otp-box">
                        <div class="otp-code">{otp}</div>
                    </div>
                    
                    <p><strong>This code will expire in {TwoFactorAuthService.OTP_EXPIRY_MINUTES} minutes.</strong></p>
                    <p>If you didn't request this code, please ignore this email or contact your administrator.</p>
                    <p><strong>Security Tip:</strong> Never share this code with anyone.</p>
                </div>
                <div class="footer">
                    <p>© 2026 PGT International (Private) Limited</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        result = email_service.send_email(
            to_email=user.email,
            subject="Your Verification Code - PGT TMS",
            html_body=html_body
        )
        
        if result["success"]:
            return {
                "success": True,
                "message": "OTP sent successfully",
                "expires_in_minutes": TwoFactorAuthService.OTP_EXPIRY_MINUTES
            }
        else:
            return {"success": False, "error": "Failed to send OTP"}
    
    @staticmethod
    def verify_otp(db: Session, user_id: int, otp: str) -> Dict:
        """Verify OTP for user"""
        # Get recent OTP settings for user
        settings = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key.like(f"2fa_otp_{user_id}_%")
        ).order_by(models.SystemSetting.id.desc()).limit(5).all()
        
        for setting in settings:
            try:
                import ast
                otp_data = ast.literal_eval(setting.setting_value)
                
                # Check if OTP matches
                if otp_data["otp"] == otp:
                    # Check if expired
                    expires_at = datetime.fromisoformat(otp_data["expires_at"])
                    if datetime.now() > expires_at:
                        return {"success": False, "error": "OTP expired"}
                    
                    # Check if already used
                    if otp_data.get("used", False):
                        return {"success": False, "error": "OTP already used"}
                    
                    # Mark as used
                    otp_data["used"] = True
                    setting.setting_value = str(otp_data)
                    db.commit()
                    
                    return {"success": True, "message": "OTP verified successfully"}
            except:
                continue
        
        return {"success": False, "error": "Invalid OTP"}
    
    @staticmethod
    def enable_2fa(db: Session, user_id: int) -> Dict:
        """Enable 2FA for user"""
        user = db.query(models.User).filter(models.User.id == user_id).first()
        
        if not user:
            return {"success": False, "error": "User not found"}
        
        # Store 2FA enabled status
        setting_key = f"2fa_enabled_{user_id}"
        setting = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key == setting_key
        ).first()
        
        if setting:
            setting.setting_value = "true"
        else:
            setting = models.SystemSetting(
                setting_key=setting_key,
                setting_value="true",
                setting_type="boolean",
                description=f"2FA enabled for user {user_id}",
                is_public=False
            )
            db.add(setting)
        
        db.commit()
        
        return {"success": True, "message": "2FA enabled successfully"}
    
    @staticmethod
    def disable_2fa(db: Session, user_id: int) -> Dict:
        """Disable 2FA for user"""
        setting_key = f"2fa_enabled_{user_id}"
        setting = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key == setting_key
        ).first()
        
        if setting:
            setting.setting_value = "false"
            db.commit()
        
        return {"success": True, "message": "2FA disabled successfully"}
    
    @staticmethod
    def is_2fa_enabled(db: Session, user_id: int) -> bool:
        """Check if 2FA is enabled for user"""
        setting_key = f"2fa_enabled_{user_id}"
        setting = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key == setting_key
        ).first()
        
        if setting and setting.setting_value == "true":
            return True
        
        return False
    
    @staticmethod
    def generate_backup_codes(db: Session, user_id: int, count: int = 10) -> Dict:
        """Generate backup codes for 2FA"""
        backup_codes = []
        for _ in range(count):
            code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            backup_codes.append(code)
        
        # Store backup codes
        setting_key = f"2fa_backup_codes_{user_id}"
        setting = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key == setting_key
        ).first()
        
        backup_data = {
            "codes": backup_codes,
            "generated_at": datetime.now().isoformat(),
            "used_codes": []
        }
        
        if setting:
            setting.setting_value = str(backup_data)
        else:
            setting = models.SystemSetting(
                setting_key=setting_key,
                setting_value=str(backup_data),
                setting_type="json",
                description=f"2FA backup codes for user {user_id}",
                is_public=False
            )
            db.add(setting)
        
        db.commit()
        
        return {
            "success": True,
            "backup_codes": backup_codes,
            "message": "Save these codes in a safe place. Each code can only be used once."
        }
    
    @staticmethod
    def verify_backup_code(db: Session, user_id: int, code: str) -> Dict:
        """Verify backup code"""
        setting_key = f"2fa_backup_codes_{user_id}"
        setting = db.query(models.SystemSetting).filter(
            models.SystemSetting.setting_key == setting_key
        ).first()
        
        if not setting:
            return {"success": False, "error": "No backup codes found"}
        
        try:
            import ast
            backup_data = ast.literal_eval(setting.setting_value)
            
            if code in backup_data["codes"] and code not in backup_data["used_codes"]:
                # Mark code as used
                backup_data["used_codes"].append(code)
                setting.setting_value = str(backup_data)
                db.commit()
                
                return {"success": True, "message": "Backup code verified"}
            else:
                return {"success": False, "error": "Invalid or used backup code"}
        except:
            return {"success": False, "error": "Failed to verify backup code"}

"""
Email Service for PGT TMS
Handles all email notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import os
from datetime import datetime

class EmailService:
    def __init__(self):
        # Email configuration (can be moved to environment variables)
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@pgtinternational.com")
        self.from_name = "PGT International TMS"
        
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: Optional[str] = None
    ) -> dict:
        """Send an email"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text and HTML parts
            if text_body:
                part1 = MIMEText(text_body, 'plain')
                msg.attach(part1)
            
            part2 = MIMEText(html_body, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return {"success": True, "message": "Email sent successfully"}
            
        except Exception as e:
            print(f"Email error: {e}")
            return {"success": False, "error": str(e)}
    
    def send_password_reset_email(self, to_email: str, reset_token: str, username: str) -> dict:
        """Send password reset email"""
        reset_link = f"http://localhost:3000/reset-password?token={reset_token}"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9fafb; padding: 30px; }}
                .button {{ 
                    display: inline-block; 
                    padding: 12px 30px; 
                    background: #dc2626; 
                    color: white; 
                    text-decoration: none; 
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>PGT International TMS</h1>
                    <p>Password Reset Request</p>
                </div>
                <div class="content">
                    <p>Hello {username},</p>
                    <p>We received a request to reset your password. Click the button below to create a new password:</p>
                    <center>
                        <a href="{reset_link}" class="button">Reset Password</a>
                    </center>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #6b7280;">{reset_link}</p>
                    <p><strong>This link will expire in 1 hour.</strong></p>
                    <p>If you didn't request this password reset, please ignore this email or contact your administrator.</p>
                </div>
                <div class="footer">
                    <p>© 2026 PGT International (Private) Limited</p>
                    <p>This is an automated email. Please do not reply.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        text_body = f"""
        PGT International TMS - Password Reset
        
        Hello {username},
        
        We received a request to reset your password.
        
        Click this link to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this password reset, please ignore this email.
        
        © 2026 PGT International (Private) Limited
        """
        
        return self.send_email(
            to_email=to_email,
            subject="Reset Your Password - PGT TMS",
            html_body=html_body,
            text_body=text_body
        )
    
    def send_payment_reminder(
        self,
        to_email: str,
        client_name: str,
        invoice_number: str,
        amount: float,
        due_date: str,
        days_overdue: int = 0
    ) -> dict:
        """Send payment reminder email"""
        status = "OVERDUE" if days_overdue > 0 else "DUE"
        urgency_color = "#dc2626" if days_overdue > 0 else "#f59e0b"
        
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9fafb; padding: 30px; }}
                .invoice-box {{ 
                    background: white; 
                    border: 2px solid {urgency_color}; 
                    padding: 20px; 
                    margin: 20px 0;
                    border-radius: 8px;
                }}
                .amount {{ font-size: 24px; font-weight: bold; color: {urgency_color}; }}
                .status {{ 
                    display: inline-block;
                    padding: 5px 15px;
                    background: {urgency_color};
                    color: white;
                    border-radius: 20px;
                    font-weight: bold;
                }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>PGT International TMS</h1>
                    <p>Payment Reminder</p>
                </div>
                <div class="content">
                    <p>Dear {client_name},</p>
                    <p>This is a friendly reminder about your pending payment:</p>
                    
                    <div class="invoice-box">
                        <p><strong>Invoice Number:</strong> {invoice_number}</p>
                        <p><strong>Amount Due:</strong> <span class="amount">PKR {amount:,.2f}</span></p>
                        <p><strong>Due Date:</strong> {due_date}</p>
                        <p><strong>Status:</strong> <span class="status">{status}</span></p>
                        {f'<p style="color: #dc2626;"><strong>Days Overdue:</strong> {days_overdue} days</p>' if days_overdue > 0 else ''}
                    </div>
                    
                    <p>Please arrange payment at your earliest convenience.</p>
                    <p>For any queries, please contact our accounts department.</p>
                    
                    <p>Thank you for your business!</p>
                </div>
                <div class="footer">
                    <p>© 2026 PGT International (Private) Limited</p>
                    <p>Phone: +92-XXX-XXXXXXX | Email: accounts@pgtinternational.com</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=to_email,
            subject=f"Payment Reminder - Invoice {invoice_number} ({status})",
            html_body=html_body
        )
    
    def send_invoice_email(
        self,
        to_email: str,
        client_name: str,
        invoice_number: str,
        amount: float,
        pdf_attachment: Optional[bytes] = None
    ) -> dict:
        """Send invoice email with PDF attachment"""
        # TODO: Add PDF attachment support
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #dc2626; color: white; padding: 20px; text-align: center; }}
                .content {{ background: #f9fafb; padding: 30px; }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>PGT International TMS</h1>
                    <p>Invoice</p>
                </div>
                <div class="content">
                    <p>Dear {client_name},</p>
                    <p>Please find attached invoice <strong>{invoice_number}</strong> for PKR {amount:,.2f}.</p>
                    <p>Thank you for your business!</p>
                </div>
                <div class="footer">
                    <p>© 2026 PGT International (Private) Limited</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(
            to_email=to_email,
            subject=f"Invoice {invoice_number} - PGT International",
            html_body=html_body
        )

# Singleton instance
email_service = EmailService()

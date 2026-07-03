"""
Email Service

Centralized email sending functionality using SMTP.
Handles templating, sending, and error handling.

Usage:
    from utils.email_service import EmailService
    
    email_service = EmailService()
    await email_service.send_verification_email(user_email, verification_code)
    await email_service.send_reminder(user_email, task_name)
"""

import logging
from typing import List, Optional, Dict, Any
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import os

from core.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)


class EmailService:
    """
    Email service for sending transactional emails.
    
    Configuration via environment variables:
    - SMTP_SERVER: Email server hostname
    - SMTP_PORT: Email server port
    - SMTP_USERNAME: Email account username
    - SMTP_PASSWORD: Email account password
    - SENDER_EMAIL: Sender email address
    - SENDER_NAME: Sender display name
    """
    
    def __init__(
        self,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        sender_email: Optional[str] = None,
        sender_name: Optional[str] = None,
    ):
        """Initialize email service with SMTP configuration"""
        self.smtp_server = smtp_server or os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", 587))
        self.username = username or os.getenv("SMTP_USERNAME")
        self.password = password or os.getenv("SMTP_PASSWORD")
        self.sender_email = sender_email or os.getenv("SENDER_EMAIL")
        self.sender_name = sender_name or os.getenv("SENDER_NAME", "VidyaGuru")
    
    async def send_verification_email(
        self,
        recipient_email: str,
        verification_code: str,
        user_name: Optional[str] = None,
    ) -> bool:
        """
        Send email verification code.
        
        Args:
            recipient_email: User's email
            verification_code: Verification code to send
            user_name: User's name for personalization
        
        Returns:
            True if sent successfully
        """
        subject = "Verify Your VidyaGuru Account"
        
        html_template = """
        <h2>Welcome to VidyaGuru!</h2>
        <p>Hi {{ user_name or 'there' }},</p>
        <p>Thank you for signing up! To complete your registration, please verify your email address using the code below:</p>
        
        <h3 style="background-color: #f0f0f0; padding: 10px; text-align: center;">{{ verification_code }}</h3>
        
        <p>Or click this link: <a href="{{ verification_link }}">Verify Email</a></p>
        
        <p>This code will expire in 24 hours.</p>
        
        <p>If you didn't sign up for VidyaGuru, please ignore this email.</p>
        
        <br>
        <p>Best regards,<br>The VidyaGuru Team</p>
        """
        
        context = {
            "user_name": user_name,
            "verification_code": verification_code,
            "verification_link": f"https://vidyaguru.app/verify?code={verification_code}",
        }
        
        return await self._send_email(
            recipient_email,
            subject,
            html_template,
            context
        )
    
    async def send_password_reset_email(
        self,
        recipient_email: str,
        reset_token: str,
        user_name: Optional[str] = None,
    ) -> bool:
        """Send password reset email with token"""
        subject = "Reset Your VidyaGuru Password"
        
        html_template = """
        <h2>Password Reset Request</h2>
        <p>Hi {{ user_name or 'there' }},</p>
        <p>We received a request to reset your password. Click the link below to set a new password:</p>
        
        <p><a href="{{ reset_link }}">Reset Password</a></p>
        
        <p>This link will expire in 1 hour.</p>
        
        <p>If you didn't request this, you can safely ignore this email.</p>
        
        <br>
        <p>Best regards,<br>The VidyaGuru Team</p>
        """
        
        context = {
            "user_name": user_name,
            "reset_link": f"https://vidyaguru.app/reset-password?token={reset_token}",
        }
        
        return await self._send_email(
            recipient_email,
            subject,
            html_template,
            context
        )
    
    async def send_challenge_completed_email(
        self,
        recipient_email: str,
        challenge_title: str,
        score: float,
        xp_earned: int,
        user_name: Optional[str] = None,
    ) -> bool:
        """Send challenge completion notification"""
        subject = f"Challenge Completed: {challenge_title}"
        
        html_template = """
        <h2>🎉 Challenge Completed!</h2>
        <p>Hi {{ user_name or 'there' }},</p>
        <p>Congratulations! You've successfully completed the challenge:</p>
        
        <h3>{{ challenge_title }}</h3>
        
        <p>
            <strong>Your Score:</strong> {{ score }}%<br>
            <strong>XP Earned:</strong> +{{ xp_earned }} XP
        </p>
        
        <p><a href="{{ challenges_link }}">View Your Solutions</a></p>
        
        <p>Keep up the great work!</p>
        
        <br>
        <p>Best regards,<br>The VidyaGuru Team</p>
        """
        
        context = {
            "user_name": user_name,
            "challenge_title": challenge_title,
            "score": round(score, 1),
            "xp_earned": xp_earned,
            "challenges_link": "https://vidyaguru.app/challenges",
        }
        
        return await self._send_email(
            recipient_email,
            subject,
            html_template,
            context
        )
    
    async def send_learning_milestone_email(
        self,
        recipient_email: str,
        milestone_name: str,
        progress_percentage: float,
        user_name: Optional[str] = None,
    ) -> bool:
        """Send learning milestone achievement email"""
        subject = f"Milestone Achieved: {milestone_name}!"
        
        html_template = """
        <h2>🏆 Milestone Achieved!</h2>
        <p>Hi {{ user_name or 'there' }},</p>
        <p>You've reached a milestone in your learning journey:</p>
        
        <h3>{{ milestone_name }}</h3>
        <p><strong>Progress:</strong> {{ progress_percentage }}% complete</p>
        
        <p>You're on track to master this learning path. Keep going!</p>
        
        <p><a href="{{ learning_link }}">Continue Learning</a></p>
        
        <br>
        <p>Best regards,<br>The VidyaGuru Team</p>
        """
        
        context = {
            "user_name": user_name,
            "milestone_name": milestone_name,
            "progress_percentage": round(progress_percentage, 1),
            "learning_link": "https://vidyaguru.app/learning",
        }
        
        return await self._send_email(
            recipient_email,
            subject,
            html_template,
            context
        )
    
    async def send_reminder_email(
        self,
        recipient_email: str,
        reminder_type: str,
        reminder_details: Dict[str, Any],
        user_name: Optional[str] = None,
    ) -> bool:
        """Send customizable reminder email"""
        reminders = {
            "incomplete_task": {
                "subject": "You have an incomplete task",
                "template": """
                <h2>📝 Reminder: Incomplete Task</h2>
                <p>Hi {{ user_name or 'there' }},</p>
                <p>You have an incomplete task waiting for you:</p>
                <h3>{{ task_name }}</h3>
                <p><a href="{{ task_link }}">Continue Task</a></p>
                """
            },
            "daily_challenge": {
                "subject": "Daily Challenge Available",
                "template": """
                <h2>⚡ Daily Challenge</h2>
                <p>Hi {{ user_name or 'there' }},</p>
                <p>A new challenge is available for you today:</p>
                <h3>{{ challenge_name }}</h3>
                <p><a href="{{ challenge_link }}">Start Challenge</a></p>
                """
            },
            "learning_path_due": {
                "subject": "Learning Path Deadline Approaching",
                "template": """
                <h2>⏰ Learning Path Reminder</h2>
                <p>Hi {{ user_name or 'there' }},</p>
                <p>Don't forget your learning path deadline is coming up:</p>
                <h3>{{ path_name }}</h3>
                <p>Deadline: {{ deadline }}</p>
                <p><a href="{{ path_link }}">Continue Learning</a></p>
                """
            }
        }
        
        if reminder_type not in reminders:
            logger.warning(f"Unknown reminder type: {reminder_type}")
            return False
        
        reminder_config = reminders[reminder_type]
        subject = reminder_config["subject"]
        html_template = reminder_config["template"]
        
        context = {
            "user_name": user_name,
            **reminder_details
        }
        
        return await self._send_email(
            recipient_email,
            subject,
            html_template,
            context
        )
    
    async def send_integrity_alert_email(
        self,
        recipient_email: str,
        alert_type: str,
        details: Dict[str, Any],
        user_name: Optional[str] = None,
    ) -> bool:
        """Send integrity alert email"""
        subject = "Account Integrity Alert"
        
        html_template = """
        <h2>⚠️ Account Integrity Alert</h2>
        <p>Hi {{ user_name or 'there' }},</p>
        <p>We've detected suspicious activity on your account:</p>
        
        <p><strong>Alert Type:</strong> {{ alert_type }}</p>
        <p><strong>Details:</strong> {{ details }}</p>
        
        <p>If this wasn't you, please secure your account immediately by changing your password.</p>
        
        <p><a href="{{ support_link }}">Contact Support</a></p>
        
        <br>
        <p>Best regards,<br>The VidyaGuru Team</p>
        """
        
        context = {
            "user_name": user_name,
            "alert_type": alert_type,
            "details": str(details),
            "support_link": "https://vidyaguru.app/support",
        }
        
        return await self._send_email(
            recipient_email,
            subject,
            html_template,
            context
        )
    
    async def _send_email(
        self,
        recipient_email: str,
        subject: str,
        html_template: str,
        context: Dict[str, Any],
    ) -> bool:
        """
        Internal method to send email with template rendering.
        
        Args:
            recipient_email: Email recipient
            subject: Email subject
            html_template: Jinja2 HTML template
            context: Template context variables
        
        Returns:
            True if sent successfully
        """
        if not self.username or not self.password or not self.sender_email:
            logger.error("Email service not configured")
            raise ExternalServiceError(
                "email",
                "Email service is not properly configured"
            )
        
        try:
            # Render template
            template = Template(html_template)
            html_content = template.render(context)
            
            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = recipient_email
            
            # Attach HTML part
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(message)
            
            logger.info(f"Email sent to {recipient_email}: {subject}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP authentication failed")
            raise ExternalServiceError(
                "email",
                "Email service authentication failed"
            )
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error: {str(e)}")
            raise ExternalServiceError(
                "email",
                f"Failed to send email: {str(e)}"
            )
        except Exception as e:
            logger.error(f"Email sending error: {str(e)}")
            raise ExternalServiceError(
                "email",
                "Failed to send email"
            )
    
    async def send_batch_emails(
        self,
        recipients: List[str],
        subject: str,
        html_template: str,
        context: Dict[str, Any],
    ) -> tuple[int, int]:
        """
        Send email to multiple recipients.
        
        Args:
            recipients: List of email addresses
            subject: Email subject
            html_template: Jinja2 HTML template
            context: Template context variables
        
        Returns:
            Tuple of (sent_count, failed_count)
        """
        sent = 0
        failed = 0
        
        for recipient in recipients:
            try:
                await self._send_email(recipient, subject, html_template, context)
                sent += 1
            except Exception as e:
                logger.error(f"Failed to send email to {recipient}: {str(e)}")
                failed += 1
        
        return sent, failed

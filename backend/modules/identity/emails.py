from django.conf import settings
from django.core.mail import send_mail

from modules.identity.models import User


def send_verification_email(user: User, raw_token: str) -> None:
    link = f"{settings.FRONTEND_URL}/verify-email?token={raw_token}"
    send_mail(
        subject="Verify your ainolez account",
        message=(
            f"Hi {user.full_name or user.username},\n\n"
            f"Welcome to ainolez! Confirm your email to start learning:\n{link}\n\n"
            "The link works for 48 hours.\n\nLearn it. Code it. Own it."
        ),
        from_email=None,
        recipient_list=[user.email],
    )


def send_password_reset_email(user: User, raw_token: str) -> None:
    link = f"{settings.FRONTEND_URL}/reset-password?token={raw_token}"
    send_mail(
        subject="Reset your ainolez password",
        message=(
            f"Hi {user.full_name or user.username},\n\n"
            f"Choose a new password here:\n{link}\n\n"
            "The link works for 1 hour. If you did not ask for this, ignore this email."
        ),
        from_email=None,
        recipient_list=[user.email],
    )

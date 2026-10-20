"""Background jobs. The token is created inside the job so it never sits in the jobs table."""

from modules.identity import emails, selectors, services
from modules.identity.models import AuthToken
from shared.jobs import job


@job("identity.send_verification_email")
def send_verification_email(payload: dict) -> None:
    user = selectors.get_user(payload["user_id"])
    if user is None or user.is_email_verified:
        return
    raw = services.issue_token(user, AuthToken.Type.VERIFY_EMAIL)
    emails.send_verification_email(user, raw)


@job("identity.send_password_reset")
def send_password_reset(payload: dict) -> None:
    user = selectors.get_user(payload["user_id"])
    if user is None:
        return
    raw = services.issue_token(user, AuthToken.Type.RESET_PASSWORD)
    emails.send_password_reset_email(user, raw)

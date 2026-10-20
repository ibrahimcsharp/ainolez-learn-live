"""Account use cases: register, verify email, log in, reset password, edit profile."""

import hashlib
import secrets
from datetime import timedelta

from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken

from modules.identity import selectors
from modules.identity.models import AuthToken, User
from shared import audit, jobs
from shared.exceptions import ServiceError

TOKEN_LIFETIME = {
    AuthToken.Type.VERIFY_EMAIL: timedelta(hours=48),
    AuthToken.Type.RESET_PASSWORD: timedelta(hours=1),
}
PROFILE_FIELDS = ("full_name", "headline", "bio", "country", "show_on_leaderboard")


def register_learner(*, email: str, username: str, password: str, full_name: str = "") -> User:
    """Create an unverified learner and queue the verification email."""
    if selectors.get_user_by_email(email):
        raise ServiceError("An account with this email already exists.", "email_taken")
    if User.objects.filter(username__iexact=username).exists():
        raise ServiceError("This username is already taken.", "username_taken")
    try:
        with transaction.atomic():
            user = User.objects.create_user(email, username, password, full_name=full_name)
            jobs.enqueue("identity.send_verification_email", {"user_id": user.pk})
            audit.record("user.registered", actor=user, entity=user)
    except IntegrityError as exc:  # two sign-ups with the same email at once
        raise ServiceError("An account with this email already exists.", "email_taken") from exc
    return user


def resend_verification(email: str) -> None:
    """Silent when the email is unknown, so accounts cannot be discovered."""
    user = selectors.get_user_by_email(email)
    if user and not user.is_email_verified:
        jobs.enqueue("identity.send_verification_email", {"user_id": user.pk})


def verify_email(raw_token: str) -> User:
    with transaction.atomic():
        user = _use_token(raw_token, AuthToken.Type.VERIFY_EMAIL)
        user.is_email_verified = True
        user.save(update_fields=["is_email_verified", "updated_at"])
        audit.record("user.email_verified", actor=user, entity=user)
    return user


def login(*, email: str, password: str, ip: str = "") -> tuple[User, RefreshToken]:
    user = selectors.get_user_by_email(email)
    if user is None:
        User().set_password(password)  # same timing as a real check
        raise ServiceError("Incorrect email or password.", "invalid_credentials", 401)
    if not user.check_password(password):
        raise ServiceError("Incorrect email or password.", "invalid_credentials", 401)
    if not user.is_active or user.is_banned:
        raise ServiceError("This account is disabled.", "account_disabled", 403)
    if not user.is_email_verified:
        raise ServiceError("Please verify your email first.", "email_not_verified", 403)

    user.last_login = timezone.now()
    user.save(update_fields=["last_login"])
    audit.record("user.login", actor=user, entity=user, ip=ip)
    return user, RefreshToken.for_user(user)


def request_password_reset(email: str) -> None:
    """Silent when the email is unknown, so accounts cannot be discovered."""
    user = selectors.get_user_by_email(email)
    if user and user.is_active:
        jobs.enqueue("identity.send_password_reset", {"user_id": user.pk})


def reset_password(raw_token: str, new_password: str) -> User:
    """Set a new password and sign the user out everywhere."""
    with transaction.atomic():
        user = _use_token(raw_token, AuthToken.Type.RESET_PASSWORD)
        user.set_password(new_password)
        user.save(update_fields=["password", "updated_at"])
        _revoke_refresh_tokens(user)
        audit.record("user.password_reset", actor=user, entity=user)
    return user


def ban_user(user_id: int, reason: str, by) -> None:
    """Stop someone from logging in and posting; signs them out everywhere."""
    user = User.objects.filter(pk=user_id).first()
    if user is None or user.is_super_admin:
        raise ServiceError("This account cannot be banned.", "cannot_ban")
    user.is_banned = True
    user.ban_reason = reason[:255]
    user.updated_by = by
    user.save(update_fields=["is_banned", "ban_reason", "updated_by", "updated_at"])
    _revoke_refresh_tokens(user)
    audit.record("user.banned", actor=by, entity=user, after={"reason": user.ban_reason})


def update_profile(user: User, **changes) -> User:
    for field in PROFILE_FIELDS:
        if field in changes:
            setattr(user, field, changes[field])
    user.updated_by = user
    user.save(update_fields=[*PROFILE_FIELDS, "updated_by", "updated_at"])
    return user


def issue_token(user: User, token_type: str) -> str:
    """Store a hashed one-time token and return the raw value for the email link."""
    raw = secrets.token_urlsafe(32)
    AuthToken.objects.create(
        user=user,
        type=token_type,
        token_hash=_hash(raw),
        expires_at=timezone.now() + TOKEN_LIFETIME[token_type],
    )
    return raw


def _use_token(raw_token: str, token_type: str) -> User:
    now = timezone.now()
    token = (
        AuthToken.objects.select_related("user")
        .filter(token_hash=_hash(raw_token), type=token_type, expires_at__gt=now)
        .first()
    )
    # The used_at filter makes the token single-use even under double clicks.
    marked = token and AuthToken.objects.filter(pk=token.pk, used_at__isnull=True).update(
        used_at=now
    )
    if not marked or token.user.deleted_at is not None:
        raise ServiceError("This link is invalid or has expired.", "invalid_token")
    return token.user


def _revoke_refresh_tokens(user: User) -> None:
    for outstanding in OutstandingToken.objects.filter(user=user, blacklistedtoken__isnull=True):
        BlacklistedToken.objects.create(token=outstanding)


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode()).hexdigest()

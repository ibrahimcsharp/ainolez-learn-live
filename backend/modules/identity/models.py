"""Tables: roles, users, auth_tokens (database/schema/0001_identity.sql)."""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from shared.models import BaseModel


class Role(models.Model):
    SUPER_ADMIN = "super_admin"
    LEARNER = "learner"

    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "roles"

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)

    def create_user(self, email, username, password, role_name=Role.LEARNER, **fields):
        user = self.model(
            email=self.normalize_email(email).lower(),
            username=username,
            role=Role.objects.get(name=role_name),
            **fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password, **fields):
        """Used by ``manage.py createsuperuser``."""
        fields.setdefault("is_email_verified", True)
        return self.create_user(email, username, password, Role.SUPER_ADMIN, **fields)


class User(AbstractBaseUser, BaseModel):
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")
    email = models.EmailField(max_length=191)
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=120, blank=True)
    headline = models.CharField(max_length=160, blank=True)
    bio = models.CharField(max_length=1000, blank=True)
    country = models.CharField(max_length=2, blank=True)
    avatar_url = models.CharField(max_length=500, blank=True)
    is_email_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)
    ban_reason = models.CharField(max_length=255, blank=True)
    show_on_leaderboard = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True, db_column="last_login_at")

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "users"

    def __str__(self):
        return self.email

    @property
    def display_name(self) -> str:
        return self.full_name or self.username

    @property
    def is_super_admin(self) -> bool:
        return self.role.name == Role.SUPER_ADMIN


class AuthToken(models.Model):
    """One-time token for email links. Only its SHA-256 hash is stored."""

    class Type(models.TextChoices):
        VERIFY_EMAIL = "verify_email"
        RESET_PASSWORD = "reset_password"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auth_tokens")
    type = models.CharField(max_length=20, choices=Type)
    token_hash = models.CharField(max_length=64, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = "auth_tokens"

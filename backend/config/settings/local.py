"""Your PC. Emails are printed to the console instead of being sent."""

from .base import *  # noqa: F403

DEBUG = True
REFRESH_COOKIE = {**REFRESH_COOKIE, "secure": False}  # noqa: F405
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

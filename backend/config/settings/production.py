"""cPanel server (staging and production). Apache terminates HTTPS."""

from .base import *  # noqa: F403

DEBUG = False
REFRESH_COOKIE = {**REFRESH_COOKIE, "secure": True}  # noqa: F405

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "tmp" / "django.log",  # noqa: F405
        }
    },
    "root": {"handlers": ["file"], "level": "WARNING"},
}

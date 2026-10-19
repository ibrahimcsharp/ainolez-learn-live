"""pytest. Uses the ainolez_test database, rebuilt from SQL on every run (see conftest.py)."""

from .local import *  # noqa: F403

DATABASES["default"]["NAME"] = env("TEST_DB_NAME", default="ainolez_test")  # noqa: F405
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]  # fast, tests only
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
REST_FRAMEWORK = {  # noqa: F405
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_THROTTLE_RATES": {
        **{scope: "1000/min" for scope in REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]},  # noqa: F405
    },
}
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
MEDIA_ROOT = BASE_DIR / "tmp" / "test-media"  # noqa: F405
ANTHROPIC_API_KEY = "test-key"  # the Claude call itself is replaced in tests

"""Settings shared by every environment. All secrets and hosts come from .env."""

from datetime import timedelta
from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/
env = environ.Env()
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "shared",
    "modules.identity",
    "modules.media",
    "modules.content_tools",
    "modules.catalog",
    "modules.assessment",
    "modules.learning",
    "modules.gamification",
    "modules.certification",
    "modules.community",
    "modules.assistant",
    "modules.ai_authoring",
    "modules.seo",
    "modules.website",
    "modules.platform_admin",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# --- Database -------------------------------------------------------------
# Our own tables are created from database/schema/*.sql (manage.py apply_schema).
# Django only creates its framework tables (auth, contenttypes, token blacklist).
DATABASES = {
    "default": {
        "ENGINE": env("DB_ENGINE", default="django.db.backends.mysql"),
        # .strip(): a stray space after a value in .env would otherwise be part of it.
        "NAME": env("DB_NAME").strip(),
        "USER": env("DB_USER").strip(),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost").strip(),
        "PORT": env("DB_PORT", default="3306"),
        "OPTIONS": {
            "charset": "utf8mb4",
            # UTC, so SQL defaults (CURRENT_TIMESTAMP) match the times Django writes.
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES', time_zone='+00:00'",
        },
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
SCHEMA_DIR = BASE_DIR.parent / "database" / "schema"

# --- Auth -----------------------------------------------------------------
AUTH_USER_MODEL = "identity.User"
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
# Email is unique per live row through UNIQUE(email, alive) in SQL, which
# Django's check cannot see.
SILENCED_SYSTEM_CHECKS = ["auth.E003"]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "EXCEPTION_HANDLER": "shared.exceptions.api_exception_handler",
    # A view is rate limited per user (or per IP for visitors) when it sets
    # throttle_scope to one of these.
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.ScopedRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {
        "auth": "20/min",  # login, register, password reset: slows password guessing
        "community": "10/min",  # new posts, replies, comments, likes, reports
        "assistant": "10/min",  # AI tutor questions (each one costs money)
        "learning": "60/min",  # exercise and quiz submissions, lesson progress
        "search": "30/min",
        "page_views": "120/min",  # the SEO lookup the website makes on every page
    },
}

# Rate-limit counters must be shared by all Passenger processes, so they live in files.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": env("CACHE_DIR", default=str(BASE_DIR / "tmp" / "cache")),
    }
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# The refresh token lives in an httpOnly cookie; the access token stays in memory.
REFRESH_COOKIE = {
    "key": "ainolez_refresh",
    "path": "/api/v1/auth/",
    "httponly": True,
    "secure": not DEBUG,
    "samesite": "Lax",
}

# --- Frontend / CORS ------------------------------------------------------
FRONTEND_URL = env("FRONTEND_URL")
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True

# --- Email ----------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=465)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_SSL = EMAIL_PORT == 465
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="ainolez <no-reply@localhost>")

# --- Background jobs ------------------------------------------------------
JOB_LOCK_FILE = BASE_DIR / "tmp" / "run_jobs.lock"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Media library ----------------------------------------------------------
# On cPanel point MEDIA_ROOT at a web-served folder, e.g. ~/api.ainolez.com/media
MEDIA_ROOT = env.path("MEDIA_ROOT", default=BASE_DIR / "media")
MEDIA_URL = env("MEDIA_URL", default="/media/")
MEDIA_MAX_MB = env.int("MEDIA_MAX_MB", default=20)

# --- Certificates -----------------------------------------------------------
# true = an admin approves each certificate before the learner gets it.
CERTIFICATES_NEED_REVIEW = env.bool("CERTIFICATES_NEED_REVIEW", default=False)

# --- Community --------------------------------------------------------------
# Members with at least this many points post without waiting for a moderator.
COMMUNITY_TRUSTED_POINTS = env.int("COMMUNITY_TRUSTED_POINTS", default=100)

# --- SEO ------------------------------------------------------------------
# The website folder (public_html on cPanel) that gets the prerendered pages,
# sitemap.xml and robots.txt. Empty = skip (e.g. on a PC without a build).
PRERENDER_DIR = env("PRERENDER_DIR", default="")

# --- AI tutor ---------------------------------------------------------------
# Never sent to the browser. Get one at https://console.anthropic.com
ANTHROPIC_API_KEY = env("ANTHROPIC_API_KEY", default="")

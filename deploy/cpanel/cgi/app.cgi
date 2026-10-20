#!/home2/ainolezc/virtualenv/apps/ainolez/backend/3.11/bin/python3.11_bin
"""Runs the API as a CGI script, for when the host has Passenger switched off.

Django starts on every request, so each one takes 1-2 seconds. Go back to Passenger
(Setup Python App) as soon as the host enables it, and delete this file.
"""

import os
import sys
from urllib.parse import unquote
from wsgiref.handlers import CGIHandler

APP_ROOT = "/home2/ainolezc/apps/ainolez/backend"
sys.path.insert(0, APP_ROOT)
os.chdir(APP_ROOT)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# .htaccess rewrites every request to this file, so take the path from the original URL.
os.environ["SCRIPT_NAME"] = ""
os.environ["PATH_INFO"] = unquote(os.environ.get("REQUEST_URI", "/").split("?", 1)[0])
# CGI hides the Authorization header; .htaccess passes it on as an environment variable.
auth = os.environ.get("HTTP_AUTHORIZATION") or os.environ.get("REDIRECT_HTTP_AUTHORIZATION")
if auth:
    os.environ["HTTP_AUTHORIZATION"] = auth

from django.core.wsgi import get_wsgi_application  # noqa: E402

CGIHandler().run(get_wsgi_application())

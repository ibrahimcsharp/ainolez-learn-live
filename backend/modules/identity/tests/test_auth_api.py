import re

import pytest
from django.core import mail
from django.core.cache import cache
from rest_framework.throttling import ScopedRateThrottle

from modules.identity.models import Role, User
from shared import jobs

pytestmark = pytest.mark.django_db
PASSWORD = "Str0ng-pass!"


def _link_token(email) -> str:
    return re.search(r"token=(\S+)", email.body).group(1)


def _login(api, email="learner@example.com", password=PASSWORD):
    return api.post("/api/v1/auth/login/", {"email": email, "password": password})


def test_register_verify_login_refresh_logout(api):
    response = api.post(
        "/api/v1/auth/register/",
        {"email": "Amina@Example.com", "username": "amina", "password": PASSWORD},
    )
    assert response.status_code == 201

    assert _login(api, "amina@example.com").json()["code"] == "email_not_verified"

    jobs.run_pending()
    token = _link_token(mail.outbox[-1])
    assert api.post("/api/v1/auth/verify-email/", {"token": token}).status_code == 200
    assert api.post("/api/v1/auth/verify-email/", {"token": token}).status_code == 400  # single use

    login = _login(api, "amina@example.com")
    assert login.status_code == 200
    assert login.json()["user"]["role"] == Role.LEARNER
    assert login.cookies["ainolez_refresh"]["httponly"]

    api.credentials(HTTP_AUTHORIZATION=f"Bearer {login.json()['access']}")
    assert api.get("/api/v1/auth/me/").json()["email"] == "amina@example.com"

    assert api.post("/api/v1/auth/refresh/").status_code == 200
    assert api.post("/api/v1/auth/logout/").status_code == 204
    assert api.post("/api/v1/auth/refresh/").status_code == 401


def test_duplicate_email_is_rejected(api, make_user):
    make_user()
    response = api.post(
        "/api/v1/auth/register/",
        {"email": "LEARNER@example.com", "username": "other", "password": PASSWORD},
    )
    assert response.json()["code"] == "email_taken"


def test_weak_password_is_rejected(api):
    response = api.post(
        "/api/v1/auth/register/",
        {"email": "a@example.com", "username": "abc", "password": "12345678"},
    )
    assert response.status_code == 400
    assert User.objects.count() == 0


def test_wrong_password(api, make_user):
    make_user()
    response = _login(api, password="wrong-password")
    assert response.status_code == 401
    assert response.json()["code"] == "invalid_credentials"


def test_password_reset_signs_out_old_sessions(api, make_user):
    make_user()
    old_session = _login(api).cookies["ainolez_refresh"].value

    api.post("/api/v1/auth/forgot-password/", {"email": "learner@example.com"})
    jobs.run_pending()
    token = _link_token(mail.outbox[-1])
    response = api.post(
        "/api/v1/auth/reset-password/", {"token": token, "password": "N3w-strong-pass"}
    )
    assert response.status_code == 200

    api.cookies["ainolez_refresh"] = old_session
    assert api.post("/api/v1/auth/refresh/").status_code == 401
    assert _login(api, password="N3w-strong-pass").status_code == 200


def test_forgot_password_does_not_reveal_unknown_email(api):
    response = api.post("/api/v1/auth/forgot-password/", {"email": "nobody@example.com"})
    assert response.status_code == 200
    jobs.run_pending()
    assert mail.outbox == []


def test_profile_update(api, make_user):
    api.force_authenticate(make_user())
    response = api.patch("/api/v1/auth/me/", {"full_name": "Amina Rahman", "country": "BD"})
    assert response.json()["full_name"] == "Amina Rahman"


def test_refresh_for_a_deleted_user_is_401_not_a_crash(api, make_user):
    user = make_user()
    _login(api)
    user.soft_delete()
    response = api.post("/api/v1/auth/refresh/")
    assert response.status_code == 401
    assert response.cookies["ainolez_refresh"].value == ""  # cookie cleared


def test_login_is_rate_limited(api, monkeypatch):
    monkeypatch.setitem(ScopedRateThrottle.THROTTLE_RATES, "auth", "3/min")
    cache.clear()
    codes = [_login(api, password="wrong").status_code for _ in range(4)]
    assert codes == [401, 401, 401, 429]
    cache.clear()

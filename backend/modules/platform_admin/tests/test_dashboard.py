import pytest

from modules.identity.models import Role

pytestmark = pytest.mark.django_db
URL = "/api/v1/admin/platform/dashboard/"
ANALYTICS = "/api/v1/admin/platform/analytics/"


def test_visitor_gets_401(api):
    assert api.get(URL).status_code == 401


def test_learner_gets_403(api, make_user):
    api.force_authenticate(make_user())
    assert api.get(URL).status_code == 403


def test_super_admin_sees_user_counts(api, make_user):
    make_user()
    admin = make_user("admin@example.com", "admin", role_name=Role.SUPER_ADMIN)
    api.force_authenticate(admin)
    assert api.get(URL).json()["users"] == {
        "learners": 1,
        "verified_learners": 1,
        "new_learners_7d": 1,
        "admins": 1,
    }


def test_analytics_has_one_value_per_day(api, make_user):
    make_user()
    api.force_authenticate(make_user("admin@example.com", "admin", role_name=Role.SUPER_ADMIN))
    data = api.get(ANALYTICS, {"days": 7}).json()
    assert len(data["days"]) == 7
    assert data["series"]["signups"][-1] == 1  # the learner made today
    assert data["totals"]["signups"] == 1
    assert all(len(values) == 7 for values in data["series"].values())


def test_analytics_falls_back_to_30_days(api, make_user):
    api.force_authenticate(make_user("admin@example.com", "admin", role_name=Role.SUPER_ADMIN))
    assert len(api.get(ANALYTICS, {"days": 5}).json()["days"]) == 30

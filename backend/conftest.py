import pytest
from django.core.management import call_command
from django.db import connection
from rest_framework.test import APIClient

from shared import schema


@pytest.fixture(scope="session")
def django_db_setup(django_db_blocker):
    """Rebuild the test database from database/schema/*.sql, then add Django's tables."""
    with django_db_blocker.unblock():
        _drop_all_tables()
        schema.apply_pending()
        call_command("migrate", verbosity=0)


def _drop_all_tables():
    name = connection.settings_dict["NAME"]
    assert name.endswith("_test"), f"Refusing to wipe non-test database '{name}'"
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            cursor.execute(f"DROP TABLE `{table}`")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def make_user(db):
    from modules.identity.models import User

    def make(email="learner@example.com", username="learner", password="Str0ng-pass!", **fields):
        fields.setdefault("is_email_verified", True)
        return User.objects.create_user(email, username, password, **fields)

    return make


@pytest.fixture
def admin_api(make_user):
    """An API client logged in as a super admin."""
    from modules.identity.models import Role

    client = APIClient()
    client.force_authenticate(make_user("admin@example.com", "admin", role_name=Role.SUPER_ADMIN))
    return client


KEEP_TABLES = {
    "roles",
    "schema_migrations",
    "django_migrations",
    "django_content_type",
    "auth_permission",
    # rows seeded by the SQL files that later tests rely on
    "seo_settings",
    "seo_pages",
    "community_settings",
}


@pytest.fixture
def committed_db(transactional_db):
    """For tests that must commit (e.g. FULLTEXT search). Empties our tables afterwards,
    because Django's own cleanup skips tables it does not manage."""
    yield
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall() if row[0] not in KEEP_TABLES]
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        for table in tables:
            cursor.execute(f"DELETE FROM `{table}`")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")

import pytest

from modules.identity.models import User

pytestmark = pytest.mark.django_db


def test_soft_deleted_user_is_hidden_and_email_can_be_reused(make_user):
    user = make_user()
    user.soft_delete()

    assert not User.objects.filter(pk=user.pk).exists()
    assert User.all_objects.filter(pk=user.pk).exists()
    make_user()  # UNIQUE(email, alive) allows the same email again


def test_restore(make_user):
    user = make_user()
    user.soft_delete()
    User.all_objects.get(pk=user.pk).restore()
    assert User.objects.filter(pk=user.pk).exists()

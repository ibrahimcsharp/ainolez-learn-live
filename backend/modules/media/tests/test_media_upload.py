import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from modules.media.models import MediaFile
from shared import jobs

pytestmark = pytest.mark.django_db
URL = "/api/v1/admin/media/files/"


def _png() -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (40, 20), "green").save(buffer, "PNG")
    return buffer.getvalue()


def test_upload_image_stores_its_size(admin_api):
    response = admin_api.post(
        URL,
        {"file": SimpleUploadedFile("logo.png", _png()), "alt_text": "Logo"},
        format="multipart",
    )
    assert response.status_code == 201
    data = response.json()
    assert (data["width"], data["height"], data["mime_type"]) == (40, 20, "image/png")
    assert data["url"].startswith("/media/uploads/")


def test_fake_image_is_refused(admin_api):
    response = admin_api.post(
        URL, {"file": SimpleUploadedFile("x.png", b"not an image")}, format="multipart"
    )
    assert response.json()["code"] == "bad_file_content"


def test_other_file_types_are_refused(admin_api):
    response = admin_api.post(
        URL, {"file": SimpleUploadedFile("x.svg", b"<svg/>")}, format="multipart"
    )
    assert response.json()["code"] == "bad_file_type"


def test_hard_delete_removes_the_file(admin_api, settings):
    media = admin_api.post(
        URL, {"file": SimpleUploadedFile("a.png", _png())}, format="multipart"
    ).json()
    stored = settings.MEDIA_ROOT / MediaFile.objects.get().file_path
    assert stored.exists()

    admin_api.post(f"{URL}{media['id']}/soft-delete/")
    admin_api.delete(f"{URL}{media['id']}/hard/", {"confirm": "a.png"})
    jobs.run_pending()
    assert not stored.exists()

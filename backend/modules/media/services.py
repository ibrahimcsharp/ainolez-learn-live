"""Media library uploads. Only checked image, PDF and MP4 files are accepted."""

import uuid
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from PIL import Image, UnidentifiedImageError

from modules.media.models import MediaFile
from shared import audit
from shared.exceptions import ServiceError

ALLOWED_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".pdf": "application/pdf",
    ".mp4": "video/mp4",
}


def upload(file, alt_text: str, by) -> MediaFile:
    extension = Path(file.name).suffix.lower()
    mime_type = ALLOWED_TYPES.get(extension)
    if mime_type is None:
        raise ServiceError("Upload a JPG, PNG, GIF, WebP, PDF or MP4 file.", "bad_file_type")
    if file.size > settings.MEDIA_MAX_MB * 1024 * 1024:
        raise ServiceError(f"Files can be at most {settings.MEDIA_MAX_MB} MB.", "file_too_large")

    width, height = _check_content(file, mime_type)
    name = timezone.now().strftime("uploads/%Y/%m/") + uuid.uuid4().hex + extension
    stored_path = default_storage.save(name, file)
    media = MediaFile.objects.create(
        file_path=stored_path,
        original_name=Path(file.name).name[:255],
        mime_type=mime_type,
        size_bytes=file.size,
        width=width,
        height=height,
        alt_text=alt_text,
        created_by=by,
        updated_by=by,
    )
    audit.record("mediafile.created", actor=by, entity=media)
    return media


def _check_content(file, mime_type: str) -> tuple[int | None, int | None]:
    """Make sure the bytes really are what the extension claims. Returns image size."""
    head = file.read(16)
    file.seek(0)
    if mime_type == "application/pdf" and not head.startswith(b"%PDF"):
        raise ServiceError("This is not a valid PDF file.", "bad_file_content")
    if mime_type == "video/mp4" and head[4:8] != b"ftyp":
        raise ServiceError("This is not a valid MP4 file.", "bad_file_content")
    if not mime_type.startswith("image/"):
        return None, None
    try:
        with Image.open(file) as image:
            image.verify()
            size = image.size
    except (UnidentifiedImageError, OSError) as exc:
        raise ServiceError("This is not a valid image.", "bad_file_content") from exc
    finally:
        file.seek(0)
    return size

"""Read queries other modules may use."""

from modules.media.models import MediaFile


def get_live_media(media_id: int) -> MediaFile | None:
    return MediaFile.objects.filter(pk=media_id, is_active=True).first()


def urls_for(media_ids) -> dict[int, str]:
    """{media_id: public URL} for live, active files."""
    files = MediaFile.objects.filter(pk__in=[i for i in media_ids if i], is_active=True)
    return {media.pk: media.url for media in files}

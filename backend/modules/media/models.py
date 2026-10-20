"""Table: media_files (database/schema/0003_media.sql)."""

from django.conf import settings
from django.db import models

from shared import jobs
from shared.models import BaseModel


class MediaFile(BaseModel):
    file_path = models.CharField(max_length=255, unique=True)
    original_name = models.CharField(max_length=255)
    mime_type = models.CharField(max_length=100)
    size_bytes = models.BigIntegerField()
    width = models.IntegerField(null=True)
    height = models.IntegerField(null=True)
    alt_text = models.CharField(max_length=255, blank=True)

    class Meta(BaseModel.Meta):
        managed = False
        db_table = "media_files"

    @property
    def url(self) -> str:
        return settings.MEDIA_URL + self.file_path

    def delete(self, *args, **kwargs):
        """A hard delete also removes the file from disk (in a background job)."""
        path = self.file_path
        result = super().delete(*args, **kwargs)
        jobs.enqueue("media.delete_file", {"file_path": path})
        return result

from django.core.files.storage import default_storage

from shared.jobs import job


@job("media.delete_file")
def delete_file(payload: dict) -> None:
    default_storage.delete(payload["file_path"])  # no error if already gone

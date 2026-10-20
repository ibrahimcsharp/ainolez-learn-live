import os
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from shared import jobs

STALE_LOCK_SECONDS = 10 * 60


class Command(BaseCommand):
    help = "Run queued background jobs. cPanel cron calls this every minute."

    def add_arguments(self, parser):
        parser.add_argument("--max-seconds", type=int, default=50)
        parser.add_argument(
            "--watch", action="store_true", help="Keep running (local development)."
        )

    def handle(self, *args, max_seconds, watch, **options):
        lock = Path(settings.JOB_LOCK_FILE)
        if not _acquire(lock):
            self.stdout.write("Another run_jobs is still running; skipping.")
            return
        try:
            while True:
                count = jobs.run_pending(max_seconds)
                if count:
                    self.stdout.write(f"Ran {count} job(s).")
                if not watch:
                    break
                lock.touch()  # keep the lock fresh while watching
                time.sleep(5)
        finally:
            lock.unlink(missing_ok=True)


def _acquire(lock: Path) -> bool:
    """Create the lock file, so cron runs never overlap. Old locks are ignored."""
    lock.parent.mkdir(parents=True, exist_ok=True)
    if lock.exists() and time.time() - lock.stat().st_mtime > STALE_LOCK_SECONDS:
        lock.unlink(missing_ok=True)
    try:
        os.close(os.open(lock, os.O_CREAT | os.O_EXCL))
    except FileExistsError:
        return False
    return True

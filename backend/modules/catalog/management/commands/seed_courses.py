from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from modules.catalog import services
from modules.identity import selectors as identity

SEED_DIR = settings.BASE_DIR.parent / "database" / "seed" / "courses"


class Command(BaseCommand):
    help = "Load the starter courses from database/seed/courses/ (skips courses that exist)."

    def add_arguments(self, parser):
        parser.add_argument("slugs", nargs="*", help="only these course folders")
        parser.add_argument("--draft", action="store_true", help="load as drafts, not published")
        parser.add_argument("--author", default="", help="email of the admin shown as author")

    def handle(self, *args, slugs, draft, author, **options):
        by = identity.get_user_by_email(author) if author else identity.first_super_admin()
        if by is None:
            raise CommandError("Create a super admin first (manage.py createsuperuser).")
        folders = sorted(p for p in SEED_DIR.iterdir() if (p / "course.json").exists())
        for folder in folders:
            if slugs and folder.name not in slugs:
                continue
            course = services.import_course_folder(folder, publish=not draft, by=by)
            message = f"added {course.title}" if course else "already there, skipped"
            self.stdout.write(f"{folder.name}: {message}")

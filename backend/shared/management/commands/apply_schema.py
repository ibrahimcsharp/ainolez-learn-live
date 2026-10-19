from django.core.management.base import BaseCommand

from shared import schema


class Command(BaseCommand):
    help = "Create or update our tables from database/schema/*.sql."

    def handle(self, *args, **options):
        applied = schema.apply_pending()
        if not applied:
            self.stdout.write("Schema is up to date.")
        for name in applied:
            self.stdout.write(self.style.SUCCESS(f"Applied {name}"))

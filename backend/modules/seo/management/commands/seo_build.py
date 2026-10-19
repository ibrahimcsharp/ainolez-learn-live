from django.core.management.base import BaseCommand

from modules.seo import prerender


class Command(BaseCommand):
    help = "Write the prerendered public pages, sitemap.xml and robots.txt (nightly cron, deploys)."

    def handle(self, *args, **options):
        self.stdout.write(f"Wrote {prerender.build()} pages.")

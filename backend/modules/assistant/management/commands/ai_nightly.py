from django.core.management.base import BaseCommand

from modules.assistant import knowledge, services


class Command(BaseCommand):
    help = "Nightly AI tutor upkeep: re-index all knowledge and delete expired chat logs."

    def handle(self, *args, **options):
        result = knowledge.index_everything()
        purged = services.purge_old_logs()
        self.stdout.write(
            f"Indexed {result['lessons']} lessons and {result['documents']} documents, "
            f"removed {result['removed']} old sources, purged {purged} old conversations."
        )

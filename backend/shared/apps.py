from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class SharedConfig(AppConfig):
    name = "shared"

    def ready(self):
        # Registers every module's @job handlers (tasks.py) and event handlers (handlers.py).
        autodiscover_modules("tasks")
        autodiscover_modules("handlers")

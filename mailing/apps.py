from django.apps import AppConfig
import os

from config.settings import SCHEDULER_AUTOSTART


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        from mailing import scheduler
        if SCHEDULER_AUTOSTART:
            scheduler.start()
        return super().ready()

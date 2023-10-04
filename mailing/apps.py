from django.apps import AppConfig
import sys

from config.settings import SCHEDULER_AUTOSTART


class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'

    def ready(self):
        from mailing import scheduler
        if SCHEDULER_AUTOSTART and 'runserver' in sys.argv:
            scheduler.start()
        return super().ready()

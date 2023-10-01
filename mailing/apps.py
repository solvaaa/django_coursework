from django.apps import AppConfig
import os

class MailingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mailing'


    def ready(self):
        from mailing import scheduler
        scheduler.start()
        return super().ready()

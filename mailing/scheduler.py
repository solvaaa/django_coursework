import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from mailing.models import Mailing



scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)


def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def start():

    scheduler.add_jobstore(DjangoJobStore(), "default")
    try:
        print("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        scheduler.shutdown()
        print("Scheduler shut down successfully!")


def send_email_job(job_id, scheduler_frequency, subject, body):
    print(f'{subject}, {body}')
    if scheduler_frequency == 'ONCE':
        scheduler.remove_job(job_id=job_id)
    mailing = Mailing.objects.get(pk=job_id)
    print(mailing)
    mailing.status = 'FIN'
    mailing.save()

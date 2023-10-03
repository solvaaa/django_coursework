from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings

from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from config.settings import SCHEDULER_ADD_CLEANING_JOB
from mailing.models import Mailing, MailingLogs
from mailing.services import get_next_datetime

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
    if SCHEDULER_ADD_CLEANING_JOB:
        scheduler.add_job(
          delete_old_job_executions,
          trigger=CronTrigger(
            day_of_week="mon", hour="00", minute="00"
          ),  # Midnight on Monday, before start of the next work week.
          id="delete_old_job_executions",
          max_instances=1,
          replace_existing=True,
        )
    try:
        print("Starting scheduler...")
        scheduler.start()
    except KeyboardInterrupt:
        print("Stopping scheduler...")
        scheduler.shutdown()
        print("Scheduler shut down successfully!")


def send_email_job(job_id, scheduler_frequency, subject, body):
    print(f'{subject}, {body}')

    attempt_time = datetime.today()
    attempt_status = True
    server_response = '200'
    mailing = Mailing.objects.get(pk=int(job_id))

    MailingLogs.objects.create(attempt_time=attempt_time,
                               attempt_status=attempt_status,
                               server_response=server_response,
                               mailing=mailing)

    if scheduler_frequency == 'ONCE':
        mailing = Mailing.objects.get(pk=job_id)
        mailing.status = 'FIN'
        mailing.save()


def start_job(job_id, time, frequency, message, email_list):
    frequencies = {
        'ONCE': 'ONCE',
        'DAILY': 'DAILY',
        'WEEKLY': 'WEEKLY',
        'MONTHLY': 'MONTHLY'
    }
    job_id = str(job_id)
    scheduler_frequency = frequencies[frequency]
    scheduler_args = [
        job_id,
        scheduler_frequency,
        message.subject,
        message.body
    ]
    if frequency == 'ONCE':
        trigger = DateTrigger(run_date=get_next_datetime(time))
    else:
        if frequency == 'DAILY':
            interval = {'days': 1}
        elif frequency == 'WEEKLY':
            interval = {'weeks': 1}
        elif frequency == 'MONTHLY':
            interval = {'days': 30}
        else:
            interval = {}
        interval['start_date'] = get_next_datetime(time) - timedelta(days=1)
        trigger = IntervalTrigger(**interval)

    scheduler.add_job(
        send_email_job,
        args=scheduler_args,
        trigger=trigger,  # Every 10 seconds
        id=job_id,  # The `id` assigned to each job MUST be unique
        max_instances=1,
        replace_existing=True,
    )


def remove_job(job_id):
    try:
        scheduler.remove_job(job_id)
    except JobLookupError:
        print(f'job {job_id} not found')

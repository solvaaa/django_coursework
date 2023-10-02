from mailing.scheduler import remove_job, start_job
from users.models import User
from mailing.models import Mailing


def remove_jobs_by_user(uid):
    if uid is not None:
        user = User.objects.get(pk=uid)
    else:
        return None

    mailings = Mailing.objects.filter(user__pk=uid)
    for mailing in mailings:
        remove_job(mailing.pk)
    return True


def add_jobs_by_user(uid):
    if uid is not None:
        user = User.objects.get(pk=uid)
    else:
        return None

    mailings = Mailing.objects.filter(user__pk=uid)
    for mailing in mailings:
        job_id = mailing.pk
        time = mailing.mailing_time
        frequency = mailing.frequency
        message = mailing.message
        email_list = []
        for client in mailing.clients.all():
            email_list.append(client.email)
        start_job(job_id, time, frequency, message, email_list)



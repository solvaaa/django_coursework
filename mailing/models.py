from django.db import models
from users.models import User

# Create your models here.
NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    email = models.EmailField(max_length=100, verbose_name='e-mail')
    name = models.CharField(max_length=100, verbose_name='ФИО', **NULLABLE)
    comment = models.CharField(max_length=100, verbose_name='комментарий', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь", **NULLABLE)

    def __str__(self):
        return f'{self.email} - {self.name}'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Mailing(models.Model):
    ONCE = 'ONCE'
    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'
    FREQUENCY_CHOICES = (
        (ONCE, 'не повторять'),
        (DAILY, 'ежедневно'),
        (WEEKLY, 'еженедельно'),
        (MONTHLY, 'ежемесячно')
    )

    CREATED = "CREAT"
    STARTED = "START"
    FINISHED = "FIN"
    STATUS_CHOICES = (
        (CREATED, 'создана'),
        (STARTED, 'запущена'),
        (FINISHED, 'завершена')
    )

    name = models.CharField(max_length=100, verbose_name='название')
    mailing_time = models.TimeField(verbose_name='время')
    frequency = models.CharField(max_length=15, choices=FREQUENCY_CHOICES,
                                 default=ONCE, verbose_name='периодичность')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                              default=CREATED, verbose_name='статус')
    message = models.ForeignKey("MailingMessage", on_delete=models.CASCADE)
    clients = models.ManyToManyField('Client', through='MailingClient', verbose_name='клиенты')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")

    def __str__(self):
        return f'{self.pk} {self.status}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class MailingMessage(models.Model):
    subject = models.CharField(max_length=200, verbose_name='тема')
    body = models.TextField(verbose_name='тело', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="пользователь")

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'


class MailingLogs(models.Model):
    attempt_time = models.DateTimeField(verbose_name='время попытки')
    attempt_status = models.BooleanField(default=False, verbose_name='статус')
    server_response = models.CharField(max_length=50, verbose_name='ответ сервера')
    mailing = models.ForeignKey("Mailing", on_delete=models.CASCADE)

    def __str__(self):
        status = 'success' if self.attempt_status else 'fail'
        return f'{self.attempt_time} - {status}. server:{self.server_response}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'


class MailingClient(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, **NULLABLE)

    def __str__(self):
        return f'{self.mailing}, {self.client}'
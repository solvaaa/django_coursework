# Generated by Django 4.2.5 on 2023-10-01 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0006_alter_mailing_mailing_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='name',
            field=models.CharField(default='rass', max_length=100, verbose_name='название'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='mailingmessage',
            name='subject',
            field=models.CharField(max_length=200, verbose_name='тема'),
        ),
        migrations.CreateModel(
            name='MailingClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mailing.client')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing')),
            ],
        ),
        migrations.AddField(
            model_name='mailing',
            name='clients',
            field=models.ManyToManyField(through='mailing.MailingClient', to='mailing.client', verbose_name='клиенты'),
        ),
    ]

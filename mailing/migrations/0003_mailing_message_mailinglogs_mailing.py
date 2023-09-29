# Generated by Django 4.2.5 on 2023-09-29 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_mailinglogs_attempt_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailingmessage'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailinglogs',
            name='mailing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing'),
        ),
    ]
# Generated by Django 5.0.7 on 2024-08-01 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auto_reply_delay',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='auto_reply_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='auto_reply_message',
            field=models.TextField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2 on 2024-10-29 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_remove_message_user_message_recipient_message_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_broadcast',
            field=models.BooleanField(default=False),
        ),
    ]
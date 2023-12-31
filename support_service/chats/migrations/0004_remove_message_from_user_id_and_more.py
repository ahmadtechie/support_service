# Generated by Django 4.2.7 on 2023-11-22 09:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chats", "0003_remove_conversation_admin_id_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="message",
            name="from_user_id",
        ),
        migrations.RemoveField(
            model_name="message",
            name="to_user_id",
        ),
        migrations.AddField(
            model_name="conversation",
            name="email",
            field=models.EmailField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="conversation",
            name="username",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="message",
            name="from_user_email",
            field=models.UUIDField(null=True),
        ),
        migrations.AddField(
            model_name="message",
            name="to_user_email",
            field=models.UUIDField(null=True),
        ),
    ]

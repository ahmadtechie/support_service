# Generated by Django 4.2.7 on 2023-11-22 11:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("chats", "0004_remove_message_from_user_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="from_user_email",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="message",
            name="to_user_email",
            field=models.EmailField(max_length=254, null=True),
        ),
    ]

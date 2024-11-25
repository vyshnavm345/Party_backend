# Generated by Django 5.0.9 on 2024-11-19 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0032_alter_candidate_phone_alter_district_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeviceToken",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("token", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="device_tokens",
                        to="accounts.member",
                    ),
                ),
            ],
        ),
    ]
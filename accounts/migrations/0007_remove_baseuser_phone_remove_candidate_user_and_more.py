# Generated by Django 5.0.9 on 2024-10-28 12:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_alter_baseuser_email"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="baseuser",
            name="phone",
        ),
        migrations.RemoveField(
            model_name="candidate",
            name="user",
        ),
        migrations.AddField(
            model_name="candidate",
            name="member",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="candidate",
                to="accounts.member",
            ),
        ),
        migrations.AddField(
            model_name="member",
            name="Nic",
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="member",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True, unique=True),
        ),
    ]

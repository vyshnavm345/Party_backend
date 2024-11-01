# Generated by Django 5.0.9 on 2024-11-01 12:10

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0014_candidate_address_candidate_education_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="date_of_birth",
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
# Generated by Django 5.0.9 on 2024-11-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0015_candidate_date_of_birth"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="email",
            field=models.EmailField(default="demo@sample.com", max_length=254),
            preserve_default=False,
        ),
    ]
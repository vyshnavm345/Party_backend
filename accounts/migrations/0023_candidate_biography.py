# Generated by Django 5.0.9 on 2024-11-04 08:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0022_alter_candidate_district_alter_member_district"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="biography",
            field=models.TextField(blank=True, null=True),
        ),
    ]
# Generated by Django 5.0.9 on 2024-10-28 11:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0005_alter_baseuser_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="baseuser",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]

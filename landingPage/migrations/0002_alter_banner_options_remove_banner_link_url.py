# Generated by Django 5.0.9 on 2024-11-11 13:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("landingPage", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="banner",
            options={
                "verbose_name": "Home page Banner",
                "verbose_name_plural": "Banners",
            },
        ),
        migrations.RemoveField(
            model_name="banner",
            name="link_url",
        ),
    ]

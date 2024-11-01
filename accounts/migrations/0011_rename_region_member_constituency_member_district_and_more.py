# Generated by Django 5.0.9 on 2024-10-29 11:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0010_otp"),
    ]

    operations = [
        migrations.RenameField(
            model_name="member",
            old_name="region",
            new_name="constituency",
        ),
        migrations.AddField(
            model_name="member",
            name="district",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="member",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                max_length=10,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="member",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="member_images/"),
        ),
    ]

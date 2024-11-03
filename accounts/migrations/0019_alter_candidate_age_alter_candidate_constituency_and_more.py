# Generated by Django 5.0.9 on 2024-11-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0018_alter_otp_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="age",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="constituency",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="date_of_birth",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="last_name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="candidate",
            name="phone",
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
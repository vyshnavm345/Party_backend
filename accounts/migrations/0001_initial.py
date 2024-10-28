# Generated by Django 5.0.9 on 2024-10-28 07:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="BaseUser",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("first_name", models.CharField(max_length=100)),
                ("last_name", models.CharField(max_length=100)),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                ("date_of_birth", models.DateField()),
                ("is_active", models.BooleanField(default=True)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("phone", models.PositiveIntegerField(unique=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Candidate",
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
                ("constituency", models.CharField(max_length=100)),
                (
                    "party_affiliation",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "election_status",
                    models.CharField(
                        choices=[
                            ("nominated", "Nominated"),
                            ("in_campaign", "In Campaign"),
                            ("elected", "Elected"),
                            ("not_elected", "Not Elected"),
                        ],
                        default="nominated",
                        max_length=50,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="candidate",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Member",
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
                (
                    "position_in_party",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("region", models.CharField(blank=True, max_length=100, null=True)),
                ("joined_on", models.DateField(auto_now_add=True)),
                ("verified_member", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="member",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]

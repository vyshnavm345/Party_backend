from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, date_of_birth, email=None, password=None):
        user = self.model(
            email=self.normalize_email(email) if email else None,
            date_of_birth=date_of_birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, date_of_birth, email=None, password=None):
        user = self.create_user(
            date_of_birth=date_of_birth,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"


class Member(models.Model):
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, related_name="member"
    )
    position_in_party = models.CharField(
        max_length=100, null=True, blank=True
    )  # e.g., "Party Leader", "Treasurer"
    region = models.CharField(max_length=100, null=True, blank=True)
    joined_on = models.DateField(auto_now_add=True)
    verified_member = models.BooleanField(default=False)
    Nic = models.CharField(max_length=50, unique=True, null=True)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position_in_party or 'Member'}"


class Candidate(models.Model):
    member = models.OneToOneField(
        Member, on_delete=models.CASCADE, related_name="candidate"
    )
    constituency = models.CharField(max_length=100)
    party_affiliation = models.CharField(max_length=100, null=True, blank=True)
    election_status = models.CharField(
        max_length=50,
        choices=[
            ("nominated", "Nominated"),
            ("in_campaign", "In Campaign"),
            ("elected", "Elected"),
            ("not_elected", "Not Elected"),
        ],
        default="nominated",
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Candidate for {self.constituency}"

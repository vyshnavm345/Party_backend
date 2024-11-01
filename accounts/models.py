from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


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
    joined_on = models.DateField(auto_now_add=True)
    verified_member = models.BooleanField(default=False)
    Nic = models.CharField(max_length=50, unique=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        null=True,
        blank=True,
    )
    district = models.CharField(max_length=100, null=True, blank=True)
    constituency = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="member_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position_in_party or 'Member'}"


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    constituency = models.CharField(max_length=100)
    party = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="candidate_images/", null=True, blank=True)
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


class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # Consider OTP valid for 5 minutes
        return timezone.now() <= self.created_at + timezone.timedelta(minutes=5)

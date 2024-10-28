from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, phone, date_of_birth, email=None, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")

        user = self.model(
            email=self.normalize_email(email) if email else None,
            date_of_birth=date_of_birth,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, date_of_birth, email=None, password=None):
        user = self.create_user(
            phone=phone,
            date_of_birth=date_of_birth,
            email=email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractUser, PermissionsMixin):  # Ensure PermissionsMixin is included
    phone = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()  # Add this field to the CustomUser
    email = models.EmailField(unique=True, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["date_of_birth"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"


class Member(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='member')  # Use CustomUser
    position_in_party = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Party Leader", "Treasurer"
    region = models.CharField(max_length=100, null=True, blank=True)
    joined_on = models.DateField(auto_now_add=True)
    verified_member = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position_in_party or 'Member'}"


class Candidate(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='candidate')  # Use CustomUser
    constituency = models.CharField(max_length=100)
    party_affiliation = models.CharField(max_length=100, null=True, blank=True)
    election_status = models.CharField(
        max_length=50,
        choices=[
            ('nominated', 'Nominated'),
            ('in_campaign', 'In Campaign'),
            ('elected', 'Elected'),
            ('not_elected', 'Not Elected')
        ],
        default='nominated'
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - Candidate for {self.constituency}"

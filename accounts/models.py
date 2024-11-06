from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet


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


# @register_snippet
# class District(models.Model):
#     name = models.CharField(max_length=100, unique=True)

#     panels = [
#         FieldPanel("name"),
#     ]
    
#     def __str__(self):
#         return self.name


class Member(models.Model):
    DISTRICT_CHOICES = [
        ("Anuradhapura", "Anuradhapura"),
        ("Badulla", "Badulla"),
        ("Batticaloa", "Batticaloa"),
        ("Colombo", "Colombo"),
        ("Digamadulla", "Digamadulla"),
        ("Galle", "Galle"),
        ("Gampaha", "Gampaha"),
        ("Hambantota", "Hambantota"),
        ("Jaffna", "Jaffna"),
        ("Kalutara", "Kalutara"),
        ("Kandy", "Kandy"),
        ("Kegalle", "Kegalle"),
        ("Kurunegala", "Kurunegala"),
        ("Matale", "Matale"),
        ("Matara", "Matara"),
        ("Moneragala", "Moneragala"),
        ("Nuwara Eliya", "Nuwara Eliya"),
        ("Polonnaruwa", "Polonnaruwa"),
        ("Puttalam", "Puttalam"),
        ("Ratnapura", "Ratnapura"),
        ("Trincomalee", "Trincomalee"),
        ("Vanni", "Vanni"),
    ]
    user = models.OneToOneField(
        BaseUser, on_delete=models.CASCADE, related_name="member"
    )
    position_in_party = models.CharField(
        max_length=100, null=True, blank=True
    )  # e.g., "Party Leader", "Treasurer"
    joined_on = models.DateField(auto_now_add=True)
    verified_member = models.BooleanField(default=False)
    nic = models.CharField(max_length=50, unique=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        null=True,
        blank=True,
    )
    district = models.CharField(
        max_length=100, choices=DISTRICT_CHOICES, null=True, blank=True
    )
    constituency = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to="member_images/", null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.position_in_party or 'Member'}"


@register_snippet
class Candidate(models.Model):
    DISTRICT_CHOICES = [
        ("Anuradhapura", "Anuradhapura"),
        ("Badulla", "Badulla"),
        ("Batticaloa", "Batticaloa"),
        ("Colombo", "Colombo"),
        ("Digamadulla", "Digamadulla"),
        ("Galle", "Galle"),
        ("Gampaha", "Gampaha"),
        ("Hambantota", "Hambantota"),
        ("Jaffna", "Jaffna"),
        ("Kalutara", "Kalutara"),
        ("Kandy", "Kandy"),
        ("Kegalle", "Kegalle"),
        ("Kurunegala", "Kurunegala"),
        ("Matale", "Matale"),
        ("Matara", "Matara"),
        ("Moneragala", "Moneragala"),
        ("Nuwara Eliya", "Nuwara Eliya"),
        ("Polonnaruwa", "Polonnaruwa"),
        ("Puttalam", "Puttalam"),
        ("Ratnapura", "Ratnapura"),
        ("Trincomalee", "Trincomalee"),
        ("Vanni", "Vanni"),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    fathers_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=800, null=True, blank=True)
    party = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(
        max_length=100, choices=DISTRICT_CHOICES, null=True, blank=True
    )
    image = models.ImageField(upload_to="candidate_images/", null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    education = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
        null=True,
        blank=True,
    )
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
    panels = [
        FieldPanel("first_name"),
        FieldPanel("last_name"),
        FieldPanel("fathers_name"),
        FieldPanel("age"),
        FieldPanel("address"),
        FieldPanel("party"),
        FieldPanel("district"),
        FieldPanel("image"),
        FieldPanel("state"),
        FieldPanel("education"),
        FieldPanel("date_of_birth"),
        FieldPanel("email"),
        FieldPanel("phone"),
        FieldPanel("biography"),
        FieldPanel("gender"),
        FieldPanel("election_status"),
    ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Candidate for {self.district}"

    # Need to set up an age function later to get the age directly from date_of_birth


class OTP(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        # Consider OTP valid for 5 minutes
        return timezone.now() <= self.created_at + timezone.timedelta(minutes=5)


# class OTP(models.Model):
#     phone_number = models.CharField(max_length=15, unique=True)
#     otp_code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(null=True, blank=True)

#     def is_valid(self):
#         # Consider OTP valid for 5 minutes
#         return timezone.now() <= self.created_at + timezone.timedelta(minutes=5)

#     def update_otp(self, new_otp_code):
#         self.otp_code = new_otp_code
#         self.created_at = timezone.now()  # Update created_at whenever the OTP is updated
#         self.save()




# set district field to null=True blank=True
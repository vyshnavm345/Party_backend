import logging

from django.utils import timezone
from django_cron import CronJobBase, Schedule

from .models import OTP


class DeleteExpiredOTP(CronJobBase):
    schedule = Schedule(run_every_mins=1440)  # 1440 minutes = 1 day
    code = "accounts.delete_expired_otp"  # Unique code for the job

    def do(self):
        # Get current time
        now = timezone.now()

        # Delete OTPs that are older than 5 minutes
        expired_otps = OTP.objects.filter(
            created_at__lt=now - timezone.timedelta(minutes=5)
        )
        count, _ = expired_otps.delete()

        # Log the result
        if count:
            logging.info(f"Deleted {count} expired OTP(s).")
        else:
            logging.info("No expired OTPs found.")

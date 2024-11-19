# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import DeviceToken

from .models import EventsFeed, NewsFeed
from .utils import send_push_notification


@receiver(post_save, sender=NewsFeed)
def send_news_notification(sender, instance, created, **kwargs):
    print("signal received")
    if created:
        # Get all device tokens
        tokens = DeviceToken.objects.values_list("token", flat=True)
        if tokens:
            # Limit the description to 100 characters
            description = instance.description or "Check out the latest news update!"
            limited_description = (
                (description[:100] + "...") if len(description) > 100 else description
            )
            notification_data = {
                "tokens": list(tokens),  # List of all FCM tokens
                "title": instance.title,
                "message": limited_description or "Check out the latest news update!",
            }
            print("pushing notification to tokens : ", list(tokens))
            send_push_notification(notification_data)


@receiver(post_save, sender=EventsFeed)
def send_events_notification(sender, instance, created, **kwargs):
    print("signal received")
    if created:
        # Get all device tokens
        tokens = DeviceToken.objects.values_list("token", flat=True)
        if tokens:
            description = instance.description or "Check out the latest news update!"
            limited_description = (
                (description[:100] + "...") if len(description) > 100 else description
            )
            notification_data = {
                "tokens": list(tokens),  # List of all FCM tokens
                "title": instance.title,
                "message": limited_description or "Check out the latest news update!",
            }
            print("pushing notification to tokens : ", list(tokens))
            send_push_notification(notification_data)

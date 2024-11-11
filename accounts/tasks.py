import requests
from celery import shared_task
from django.conf import settings


@shared_task()
def send_otp_via_textlk(phone_number, otp):
    url = settings.TEXTLK_API_URL
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {settings.TEXTLK_API_TOKEN}",
    }
    payload = {
        "recipient": phone_number,
        "message": f"Your OTP is {otp}",
        "sender_id": settings.TEXTLK_SENDER_ID,
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None

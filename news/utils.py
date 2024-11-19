import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
from pathlib import Path
from accounts.models import DeviceToken


def send_push_notification(notification_payload):
    
    cred_path = settings.FIREBASE_CREDENTIALS_PATH

    if not Path(cred_path).exists():
        raise FileNotFoundError(f"Firebase credentials not found at {cred_path}")

    # Initialize Firebase Admin SDK if not already initialized
    if not firebase_admin._apps:
        firebase_credentials = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(firebase_credentials)

    tokens = notification_payload["tokens"]
    batch_size = 500  # FCM allows a maximum of 500 tokens per multicast message

    for i in range(0, len(tokens), batch_size):
        batch_tokens = tokens[i:i + batch_size]
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=notification_payload["title"],
                body=notification_payload["message"]
            ),
            tokens=batch_tokens
        )
        
    response = messaging.send_each_for_multicast(message)

    # Log the results
    print(f"Successfully sent messages: {response.success_count}, failed: {response.failure_count}")

    if response.failure_count > 0:
        for idx, resp in enumerate(response.responses):
            if not resp.success:
                print(f"Failed to send notification to token: {notification_payload['tokens'][idx]}")

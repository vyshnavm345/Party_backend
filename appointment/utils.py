from django.conf import settings
from django.core.mail import send_mail


def send_appointment_email(appointment):
    subject = f"New Appointment Request from {appointment.name}"
    message = (
        f"Name: {appointment.name}\n"
        f"Phone: {appointment.phone}\n"
        f"Email: {appointment.email}\n"
        f"Gender: {appointment.get_gender_display()}\n"
        f"Appointment Date: {appointment.appointment_date}\n"
        f"Appointment Time: {appointment.appointment_time}\n"
        f"Message: {appointment.message if appointment.message else 'No message provided'}\n"
    )

    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email: {e}")

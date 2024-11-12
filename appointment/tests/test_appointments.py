import pytest
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from appointment.models import Appointment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_get_appointments(api_client):
    # Arrange: Create sample appointments
    Appointment.objects.create(
        name="John Doe",
        phone="1234567890",
        email="johndoe@example.com",
        gender="M",
        appointment_date="2024-11-15",
        appointment_time="15:00",
        message="Checkup",
    )

    # Act: Send GET request
    response = api_client.get(reverse("appointment-create"))

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "John Doe"


@pytest.mark.django_db
def test_create_appointment(api_client, mocker):
    # Arrange: Mock the email sending function
    send_email_mock = mocker.patch(
        "appointment.views.send_appointment_email", return_value=None
    )

    # Data for creating an appointment
    data = {
        "name": "Jane Doe",
        "phone": "0987654321",
        "email": "janedoe@example.com",
        "gender": "F",
        "appointment_date": "2024-12-01",
        "appointment_time": "10:30",
        "message": "Consultation",
    }

    # Act: Send POST request
    response = api_client.post(reverse("appointment-create"), data, format="json")

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Jane Doe"

    # Check if the appointment was created in the database
    appointment = Appointment.objects.get(email="janedoe@example.com")
    assert appointment.name == "Jane Doe"
    assert appointment.phone == "0987654321"

    # Assert that the send_appointment_email task was called
    send_email_mock.assert_called_once_with(appointment.id)


@pytest.mark.django_db
def test_create_appointment_invalid_data(api_client):
    # Arrange: Provide invalid data (missing email)
    data = {
        "name": "Invalid User",
        "phone": "1234567890",
        "gender": "M",
        "appointment_date": "2024-11-10",
        "appointment_time": "14:00",
        "message": "",
    }

    # Act: Send POST request with invalid data
    response = api_client.post(reverse("appointment-create"), data, format="json")

    # Assert: Expect 400 Bad Request
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_send_appointment_email(settings):
    # Arrange: Set up test email backend and admin email
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    settings.EMAIL_HOST_USER = "test@example.com"
    settings.ADMIN_EMAIL = "admin@example.com"

    # Create a test appointment
    appointment = Appointment.objects.create(
        name="Email Test",
        phone="1234567890",
        email="testuser@example.com",
        gender="M",
        appointment_date="2024-11-25",
        appointment_time="12:00",
        message="Testing email",
    )

    # Act: Call the email sending function
    from appointment.tasks import send_appointment_email

    send_appointment_email(appointment.id)

    # Assert: Check if the email was sent
    assert len(mail.outbox) == 1
    email = mail.outbox[0]
    assert email.subject == f"New Appointment Request from {appointment.name}"
    assert "Email Test" in email.body
    assert email.to == [settings.ADMIN_EMAIL]

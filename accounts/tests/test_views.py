import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import OTP, Member


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def valid_phone_number():
    return "1234567890"


@pytest.fixture
def valid_otp_code(valid_phone_number):
    otp_code = "123456"
    OTP.objects.create(phone_number=valid_phone_number, otp_code=otp_code)
    return otp_code


@pytest.fixture
def user_data():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "date_of_birth": "1990-01-01",
    }


@pytest.fixture
def member_data(user_data, valid_phone_number):
    return {
        "user": user_data,
        "position_in_party": "Party Leader",
        "region": "North",
        "Nic": "123456789",
        "phone": valid_phone_number,
        "gender": "male",
        "district": "District A",
        "constituency": "Constituency 1",
        "image": None,
    }


@pytest.mark.django_db
class TestOTPViews:
    def test_send_otp(self, client, valid_phone_number):
        url = reverse("send-otp")
        response = client.post(url, {"phone_number": valid_phone_number})

        assert response.status_code == status.HTTP_200_OK
        assert response.data["detail"] == "OTP sent successfully."
        otp = OTP.objects.get(phone_number=valid_phone_number)
        assert otp is not None

    def test_verify_otp_success(self, client, valid_phone_number, valid_otp_code):
        url = reverse("verify-otp")
        response = client.post(
            url, {"phone_number": valid_phone_number, "otp_code": valid_otp_code}
        )

        assert response.status_code == status.HTTP_200_OK
        assert "detail" in response.data

    def test_verify_otp_invalid(self, client, valid_phone_number):
        OTP.objects.create(phone_number="3698521470", otp_code="111111")

        url = reverse("verify-otp")
        response = client.post(
            url, {"phone_number": "3698521470", "otp_code": "000000"}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Invalid or expired OTP."

    def test_verify_otp_expired(self, client, valid_phone_number, valid_otp_code):
        otp = OTP.objects.get(phone_number=valid_phone_number)
        otp.created_at = timezone.now() - timezone.timedelta(minutes=6)
        otp.save()

        url = reverse("verify-otp")
        response = client.post(
            url, {"phone_number": valid_phone_number, "otp_code": valid_otp_code}
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data["detail"] == "Invalid or expired OTP."


@pytest.mark.django_db
class TestMemberRegistration:
    def test_member_registration(self, client, member_data):
        url = reverse("register")
        response = client.post(url, member_data, format="json")

        assert response.status_code == status.HTTP_201_CREATED
        assert "user" in response.data
        assert response.data["phone"] == member_data["phone"]
        assert response.data["gender"] == member_data["gender"]
        assert response.data["district"] == member_data["district"]
        assert response.data["constituency"] == member_data["constituency"]

        member = Member.objects.get(phone=member_data["phone"])
        assert member is not None
        assert member.user.email == member_data["user"]["email"]
        assert member.gender == member_data["gender"]
        assert member.district == member_data["district"]
        assert member.constituency == member_data["constituency"]

    def test_member_registration_existing_phone(self, client, member_data):
        url = reverse("register")
        client.post(url, member_data, format="json")

        response = client.post(url, member_data, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        # assert response.data["detail"] == "Phone number already exists."  # Uncomment and update if necessary

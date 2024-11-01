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
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "date_of_birth": "1998-02-02",
        "password": "password123",
        "position_in_party": "Party Leader",
        "Nic": "980330330V",
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
        assert "existing_user" in response.data

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

        # Check for a successful registration
        assert response.status_code == status.HTTP_201_CREATED

        # Check for fields in the flattened response structure
        assert "first_name" in response.data
        assert "last_name" in response.data
        assert response.data["phone"] == member_data["phone"]
        assert response.data["gender"] == member_data["gender"]
        assert response.data["district"] == member_data["district"]
        assert response.data["constituency"] == member_data["constituency"]

        # Check that a member was created with the expected data
        member = Member.objects.get(phone=member_data["phone"])
        assert member is not None
        assert member.user.email == member_data["email"]
        assert member.gender == member_data["gender"]
        assert member.district == member_data["district"]
        assert member.constituency == member_data["constituency"]

    def test_member_registration_existing_phone(self, client, member_data):
        url = reverse("register")

        # Register the member first time
        client.post(url, member_data, format="json")

        # Modify member_data to have a different email and try registering again
        member_data["email"] = "new_email@example.com"
        response = client.post(url, member_data, format="json")

        # Check for duplicate phone number error
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_member_registration_invalid_nic(self, client, member_data):
        url = reverse("register")

        # Test with an invalid NIC
        invalid_nics = [
            "12345678",  # Too short
            "12345678901",  # Too long
            "1234567a89",  # Invalid characters
            "123456789v",  # Invalid ending
            "987654321",  # Valid length but invalid for your case
        ]

        for nic in invalid_nics:
            member_data["Nic"] = nic
            response = client.post(url, member_data, format="json")
            assert response.status_code == status.HTTP_400_BAD_REQUEST
            assert response.data["detail"] == "Invalid NIC"

    def test_member_registration_nic_dob_gender_mismatch(self, client, member_data):
        url = reverse("register")

        # Test with a valid NIC but incorrect DOB and gender
        member_data["Nic"] = "123456789"  # Set a NIC that you know is valid
        member_data["date_of_birth"] = "2000-01-01"  # DOB does not match NIC info
        member_data["gender"] = "female"  # Gender does not match NIC info

        response = client.post(url, member_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert (
            response.data["reason"] == "Date of birth does not match NIC"
            or response.data["reason"] == "Gender does not match NIC information"
        )


# @pytest.mark.django_db
# class TestNICVerification:
#     def test_nic_verification_success(self, client, member_data):
#         url = reverse("nic-verification")
#         member_data["Nic"] = "980330330V"  # Use a valid NIC for testing
#         # Add the necessary fields
#         member_data["gender"] = "male"  # or "female"
#         member_data["date_of_birth"] = "1998-02-02"  # Example date

#         response = client.post(url, member_data)
#     # Add assertions here


#     def test_nic_verification_invalid(self, client):
#         url = reverse("nic-verification")

#         # Test with invalid NICs
#         invalid_nics = [
#             "12345678",  # Too short
#             "12345678901",  # Too long
#             "1234567a89",  # Invalid characters
#             "123456789v",  # Invalid ending
#             "987654321",  # Valid length but invalid for your case
#         ]

#         for nic in invalid_nics:
#             member_data["Nic"] = nic
#             member_data["gender"] = "male"  # or "female"
#             member_data["date_of_birth"] = "1998-02-02"

#             response = client.post(url, member_data)
#             assert response.status_code == status.HTTP_400_BAD_REQUEST
#             assert response.data["detail"] == "Invalid NIC"


# @pytest.mark.django_db
# class TestMemberRegistration:
#     def test_member_registration(self, client, member_data):
#         # First, verify the NIC
#         nic_verification_url = reverse("nic-verification")
#         response = client.post(nic_verification_url, {"nic": member_data["Nic"]})
#         assert response.status_code == status.HTTP_200_OK

#         url = reverse("register")
#         response = client.post(url, member_data, format="json")

#         # Check for a successful registration
#         assert response.status_code == status.HTTP_201_CREATED
#         # Check for fields in the flattened response structure
#         assert "first_name" in response.data
#         assert "last_name" in response.data
#         assert response.data["phone"] == member_data["phone"]
#         assert response.data["gender"] == member_data["gender"]
#         assert response.data["district"] == member_data["district"]
#         assert response.data["constituency"] == member_data["constituency"]

#         # Check that a member was created with the expected data
#         member = Member.objects.get(phone=member_data["phone"])
#         assert member is not None
#         assert member.user.email == member_data["email"]
#         assert member.gender == member_data["gender"]
#         assert member.district == member_data["district"]
#         assert member.constituency == member_data["constituency"]

#     def test_member_registration_existing_phone(self, client, member_data):
#         # First, verify the NIC
#         nic_verification_url = reverse("nic-verification")
#         response = client.post(nic_verification_url, {"nic": member_data["Nic"]})
#         assert response.status_code == status.HTTP_200_OK

#         url = reverse("register")

#         # Register the member first time
#         client.post(url, member_data, format="json")

#         # Modify member_data to have a different email and try registering again
#         member_data["email"] = "new_email@example.com"
#         response = client.post(url, member_data, format="json")

#         # Check for duplicate phone number error
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#     def test_member_registration_invalid_nic(self, client, member_data):
#         url = reverse("register")

#         # Test with an invalid NIC
#         invalid_nics = [
#             "12345678",  # Too short
#             "12345678901",  # Too long
#             "1234567a89",  # Invalid characters
#             "123456789v",  # Invalid ending
#             "987654321",  # Valid length but invalid for your case
#         ]

#         for nic in invalid_nics:
#             member_data["Nic"] = nic
#             # Verify the NIC first
#             nic_verification_url = reverse("nic-verification")
#             response = client.post(nic_verification_url, {"nic": nic})
#             assert response.status_code == status.HTTP_400_BAD_REQUEST  # Expect failure on NIC verification

#             # Attempt to register with the invalid NIC
#             response = client.post(url, member_data, format="json")
#             assert response.status_code == status.HTTP_400_BAD_REQUEST
#             assert response.data["detail"] == "Invalid NIC"

#     def test_member_registration_nic_dob_gender_mismatch(self, client, member_data):
#         # First, verify the NIC
#         nic_verification_url = reverse("nic-verification")
#         response = client.post(nic_verification_url, {"nic": member_data["Nic"]})
#         assert response.status_code == status.HTTP_200_OK

#         url = reverse("register")

#         # Test with a valid NIC but incorrect DOB and gender
#         member_data["Nic"] = "123456789"  # Set a NIC that you know is valid
#         member_data["date_of_birth"] = "2000-01-01"  # DOB does not match NIC info
#         member_data["gender"] = "female"  # Gender does not match NIC info

#         response = client.post(url, member_data, format="json")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert (
#             response.data["reason"] == "Date of birth does not match NIC"
#             or response.data["reason"] == "Gender does not match NIC information"
#         )

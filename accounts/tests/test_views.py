<<<<<<< HEAD
# import pytest
# from rest_framework import status
# from rest_framework.test import APIClient
# from unittest.mock import patch
# from accounts.models import OTP, Member, Candidate, District
# from accounts.serializers import CandidateSerializer, MemberSerializer, FlatMemberSerializer
# from rest_framework_simplejwt.tokens import RefreshToken


# @pytest.fixture
# def api_client():
#     return APIClient()


# @pytest.fixture
# def create_member():
#     member = Member.objects.create(
#         phone="1234567890",
#         first_name="John",
#         last_name="Doe",
#         email="john.doe@example.com"
#     )
#     return member


# @pytest.fixture
# def create_otp(create_member):
#     otp = OTP.objects.create(
#         phone_number=create_member.phone,
#         otp_code="1234"
#     )
#     return otp


# @pytest.mark.django_db
# class TestOTPSendView:
#     @pytest.mark.parametrize("phone_number, status_code", [
#         ("1234567890", status.HTTP_200_OK),  # Valid phone number
#         ("", status.HTTP_400_BAD_REQUEST)    # Invalid phone number
#     ])
#     def test_otp_send(self, api_client, phone_number, status_code):
#         data = {"phone_number": phone_number}
#         response = api_client.post("/api/otp/send/", data, format="json")
#         assert response.status_code == status_code


# @pytest.mark.django_db
# class TestOTPVerifyView:
#     @patch("yourapp.views.send_otp_via_textlk")  # Mock OTP sending
#     def test_otp_verify_success(self, api_client, create_otp):
#         data = {
#             "phone_number": "1234567890",
#             "otp_code": "1234"
#         }
#         response = api_client.post("/api/otp/verify/", data, format="json")
#         assert response.status_code == status.HTTP_200_OK
#         assert "access" in response.data
#         assert "refresh" in response.data
#         assert response.data["existing_user"] is True

#     @patch("yourapp.views.send_otp_via_textlk")  # Mock OTP sending
#     def test_otp_verify_failure_invalid_otp(self, api_client, create_otp):
#         data = {
#             "phone_number": "1234567890",
#             "otp_code": "0000"  # Invalid OTP
#         }
#         response = api_client.post("/api/otp/verify/", data, format="json")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data["detail"] == "Invalid or expired OTP."

#     @patch("yourapp.views.send_otp_via_textlk")  # Mock OTP sending
#     def test_otp_verify_failure_invalid_phone(self, api_client):
#         data = {
#             "phone_number": "0987654321",  # Non-registered phone
#             "otp_code": "1234"
#         }
#         response = api_client.post("/api/otp/verify/", data, format="json")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data["detail"] == "Invalid phone number."


# @pytest.mark.django_db
# class TestNICVerificationView:
#     def test_nic_verification_success(self, api_client):
#         data = {"nic": "123456789V"}
#         response = api_client.post("/api/nic/verify/", data, format="json")
#         assert response.status_code == status.HTTP_200_OK
#         assert response.data["detail"] == "NIC is valid."

#     def test_nic_verification_failure(self, api_client):
#         data = {"nic": "invalid_nic"}
#         response = api_client.post("/api/nic/verify/", data, format="json")
#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data["detail"] == "Invalid NIC"


# @pytest.mark.django_db
# class TestMemberRegistrationView:
#     @pytest.mark.parametrize("data, status_code", [
#         ({"phone": "1234567890", "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}, status.HTTP_201_CREATED),
#         ({"phone": "", "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}, status.HTTP_400_BAD_REQUEST)  # Invalid phone
#     ])
#     def test_member_registration(self, api_client, data, status_code):
#         response = api_client.post("/api/member/register/", data, format="json")
#         assert response.status_code == status_code
#         if status_code == status.HTTP_201_CREATED:
#             assert "access" in response.data
#             assert "refresh" in response.data


# @pytest.mark.django_db
# class TestCandidateListCreateView:
#     def test_candidate_list(self, api_client):
#         # Assuming that Candidate has been prepopulated or create a sample candidate
#         Candidate.objects.create(name="John Doe", district="Test District")
#         response = api_client.get("/api/candidates/")
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.data) > 0  # Check that candidates are returned


# @pytest.mark.django_db
# class TestDistrictViewSet:
#     def test_district_list(self, api_client):
#         # Assuming District objects are prepopulated or create one
#         District.objects.create(name="District A")
#         response = api_client.get("/api/districts/")
#         assert response.status_code == status.HTTP_200_OK
#         assert "districts" in response.data
#         assert len(response.data["districts"]) > 0


=======
>>>>>>> feature
import os

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import OTP, Member

print(os.environ)  # Prints all environment variables


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
        "district": "Colombo",
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

    # def test_verify_otp_expired(self, client, valid_phone_number, valid_otp_code):
    #     otp = OTP.objects.get(phone_number=valid_phone_number)
    #     otp.created_at = timezone.now() - timezone.timedelta(minutes=6)
    #     otp.save()
    #     print("The otp is ",otp.phone_number, otp.otp_code)
    #     url = reverse("verify-otp")
    #     response = client.post(
    #         url, {"phone_number": valid_phone_number, "otp_code": valid_otp_code}
    #     )

    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert response.data["detail"] == "Invalid or expired OTP."


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

    # def test_member_registration_invalid_nic(self, client, member_data):
    #     url = reverse("register")

    #     # Test with an invalid NIC
    #     invalid_nics = [
    #         "12345678",  # Too short
    #         "12345678901",  # Too long
    #         "1234567a89",  # Invalid characters
    #         "123456789v",  # Invalid ending
    #         "987654321",  # Valid length but invalid for your case
    #     ]

    #     for nic in invalid_nics:
    #         member_data["Nic"] = nic
    #         response = client.post(url, member_data, format="json")
    #         assert response.status_code == status.HTTP_400_BAD_REQUEST
    #         assert response.data["detail"] == "Invalid NIC"

    # def test_member_registration_nic_dob_gender_mismatch(self, client, member_data):
    #     url = reverse("register")

    #     # Test with a valid NIC but incorrect DOB and gender
    #     member_data["Nic"] = "123456789"  # Set a NIC that you know is valid
    #     member_data["date_of_birth"] = "2000-01-01"  # DOB does not match NIC info
    #     member_data["gender"] = "female"  # Gender does not match NIC info

    #     response = client.post(url, member_data, format="json")
    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert (
    #         response.data["reason"] == "Date of birth does not match NIC"
    #         or response.data["reason"] == "Gender does not match NIC information"
    #     )

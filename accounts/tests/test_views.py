import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import OTP, Candidate, District, Member


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
def valid_nic_data():
    return {
        "Nic": "123456789V",  # Example of a valid old NIC
        "date_of_birth": "1990-05-12",  # Example DOB that matches the NIC
        "gender": "male",  # Example gender that matches the NIC
    }


@pytest.fixture
def invalid_nic_data():
    return {
        "Nic": "12345678",  # Invalid NIC length
        "date_of_birth": "1990-05-12",  # Valid DOB, but NIC is invalid
        "gender": "male",  # Gender is valid, but NIC is incorrect
    }


@pytest.fixture
def mismatched_dob_data():
    return {
        "Nic": "123456789V",  # Example of a valid NIC
        "date_of_birth": "1991-05-12",  # Mismatched DOB
        "gender": "male",  # Gender is valid, but DOB is incorrect
    }


@pytest.fixture
def mismatched_gender_data():
    return {
        "Nic": "123456789V",  # Example of a valid NIC
        "date_of_birth": "1990-05-12",  # Matching DOB
        "gender": "female",  # Gender mismatched with NIC (which indicates male)
    }


@pytest.fixture
def invalid_dob_format_data():
    return {
        "Nic": "123456789V",  # Example of a valid NIC
        "date_of_birth": "12-05-1990",  # Invalid DOB format
        "gender": "male",  # Gender is valid, but DOB format is incorrect
    }


@pytest.fixture
def missing_details_data():
    return {
        "Nic": "123456789V",  # Missing date_of_birth and gender
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


@pytest.mark.django_db
class TestMemberRegistration:
    def test_member_registration(self, client, member_data):
        # Create the required district beforehand
        District.objects.get_or_create(name="Colombo")
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
        assert member.district.name == member_data["district"]
        assert member.constituency == member_data["constituency"]

    def test_member_registration_existing_phone(self, client, member_data):
        # Create the required district beforehand
        District.objects.get_or_create(name="Colombo")
        url = reverse("register")

        # Register the member first time
        client.post(url, member_data, format="json")

        # Modify member_data to have a different email and try registering again
        member_data["email"] = "new_email@example.com"
        response = client.post(url, member_data, format="json")

        # Check for duplicate phone number error
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class NICVerificationViewTests(TestCase):
    def setUp(self):
        """Set up the test client and any required test data."""
        self.client = APIClient()
        self.url = reverse("nic-verification")

    def test_nic_verification_valid_data(self):
        """Test for valid NIC."""
        valid_nic_data = {
            "Nic": "123456789V",  # Example of a valid old NIC
            "date_of_birth": "1912-12-10",  # Example DOB that matches the NIC
            "gender": "male",  # Example gender that matches the NIC
        }

        response = self.client.post(self.url, valid_nic_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "NIC is valid.")

    def test_nic_verification_invalid_old_nic_format(self):
        """Test invalid NIC format (old NIC)."""
        invalid_nic_data = {
            "Nic": "12345678",  # Invalid NIC length
            "date_of_birth": "1990-05-12",  # Valid DOB, but NIC is invalid
            "gender": "male",  # Gender is valid, but NIC is incorrect
        }

        response = self.client.post(self.url, invalid_nic_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid NIC")
        self.assertEqual(response.data["reason"], "Invalid NIC length")

    def test_nic_verification_invalid_length(self):
        """Test invalid NIC length."""
        invalid_nic_data = {
            "Nic": "12345678",  # Invalid NIC length
            "date_of_birth": "1990-05-12",  # Valid DOB, but NIC is invalid
            "gender": "male",  # Gender is valid, but NIC is incorrect
        }

        response = self.client.post(self.url, invalid_nic_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid NIC")
        self.assertEqual(response.data["reason"], "Invalid NIC length")

    def test_nic_verification_mismatched_dob(self):
        """Test for mismatched date of birth."""
        mismatched_dob_data = {
            "Nic": "123456789V",  # Example of a valid NIC
            "date_of_birth": "1991-05-12",  # Mismatched DOB
            "gender": "male",  # Gender is valid, but DOB is incorrect
        }

        response = self.client.post(self.url, mismatched_dob_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid NIC")
        self.assertEqual(response.data["reason"], "Date of birth does not match NIC")

    def test_nic_verification_mismatched_gender(self):
        """Test for mismatched gender."""
        mismatched_gender_data = {
            "Nic": "123456789V",  # Example of a valid NIC
            "date_of_birth": "1912-12-10",  # Matching DOB
            "gender": "female",  # Gender mismatched with NIC (which indicates male)
        }

        response = self.client.post(self.url, mismatched_gender_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid NIC")
        self.assertEqual(
            response.data["reason"], "Gender does not match NIC information"
        )

    def test_nic_verification_invalid_dob_format(self):
        """Test for invalid date of birth format."""
        invalid_dob_format_data = {
            "Nic": "123456789V",  # Example of a valid NIC
            "date_of_birth": "12-05-1990",  # Invalid DOB format
            "gender": "male",  # Gender is valid, but DOB format is incorrect
        }

        response = self.client.post(self.url, invalid_dob_format_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid NIC")
        self.assertEqual(response.data["reason"], "Date of birth does not match NIC")

    def test_nic_verification_missing_details(self):
        """Test for missing details (NIC is provided but other details are missing)."""
        missing_details_data = {
            "Nic": "123456789V",  # Missing date_of_birth and gender
        }

        response = self.client.post(self.url, missing_details_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid NIC")
        self.assertEqual(response.data["reason"], "Missing required fields")


@pytest.mark.django_db
class TestCandidateViews:
    # Setup the initial test data
    @pytest.fixture(autouse=True)
    def setUp(self):
        # Create a district for testing
        self.district = District.objects.create(name="Test District")
        # Create candidates for testing
        self.candidate_1 = Candidate.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="1234567890",
            district=self.district,
            election_status="nominated",
        )
        self.candidate_2 = Candidate.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@example.com",
            phone="0987654321",
            district=self.district,
            election_status="in_campaign",
        )
        self.client = APIClient()

    # Test the list and create view
    def test_candidate_list_create(self):
        # Test GET request
        url = reverse("candidate-list-create")
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # There should be two candidates in the response

        # Test filtering by district name
        response = self.client.get(url, {"district": "Test District"})
        assert response.status_code == status.HTTP_200_OK
        assert (
            len(response.data) == 2
        )  # Candidates from 'Test District' should be listed

        # Test POST request for creating a new candidate
        new_candidate_data = {
            "first_name": "Mike",
            "last_name": "Johnson",
            "email": "mike.johnson@example.com",
            "phone": "1122334455",
            "district": self.district.id,
            "election_status": "nominated",
        }
        response = self.client.post(url, new_candidate_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["first_name"] == "Mike"
        assert response.data["last_name"] == "Johnson"

    # Test the detail view
    def test_candidate_detail(self):
        url = reverse("candidate-detail", kwargs={"pk": self.candidate_1.pk})

        # Test GET request
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "John"
        assert response.data["last_name"] == "Doe"

        # Test PUT request for updating candidate details
        updated_data = {
            "first_name": "John",
            "last_name": "Updated Doe",
            "email": "john.updated@example.com",
            "phone": "1234567890",
            "district": self.district.id,
            "election_status": "in_campaign",
        }
        response = self.client.put(url, updated_data, format="json")
        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "John"
        assert response.data["last_name"] == "Updated Doe"

        # Test DELETE request for deleting candidate
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Candidate.objects.count() == 1  # Only one candidate should remain

    # Test validation errors on create view
    def test_candidate_create_validation_error(self):
        url = reverse("candidate-list-create")
        invalid_data = {
            "first_name": "Invalid",
            "email": "invalid.email",  # Invalid email format
            "phone": "not_a_number",  # Invalid phone format
        }
        response = self.client.post(url, invalid_data, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data  # Email validation error should be in response
        assert "phone" in response.data  # Phone validation error should be in response

    # Test the filtering by district functionality
    def test_filter_by_district(self):
        url = reverse("candidate-list-create")
        response = self.client.get(url, {"district": self.district.name})
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Both candidates are from the same district

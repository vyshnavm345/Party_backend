import random

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import OTP, Candidate, Member
from .serializers import (
    CandidateSerializer,
    FlatMemberSerializer,
    MemberSerializer,
    OTPSendSerializer,
    OTPVerifySerializer,
)
from .utils import nest_member_data, send_otp_via_textlk, validate_nic


class OTPSendView(generics.GenericAPIView):
    serializer_class = OTPSendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp_code = str(random.randint(1000, 9999))  # Generate otp

        # Send OTP to the phone number
        # print(f"Sending OTP {otp_code} to {phone_number}")
        send_otp_via_textlk(phone_number, otp_code)

        # Save OTP to database
        OTP.objects.update_or_create(
            phone_number=phone_number, defaults={"otp_code": otp_code}
        )

        return Response({"detail": "OTP sent successfully."}, status=status.HTTP_200_OK)


class OTPVerifyView(generics.GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp_code = serializer.validated_data["otp_code"]

        try:
            otp = OTP.objects.get(phone_number=phone_number)
        except OTP.DoesNotExist:
            return Response(
                {"detail": "Invalid phone number."}, status=status.HTTP_400_BAD_REQUEST
            )

        if otp.is_valid() and otp.otp_code == otp_code:
            # if the user is new proceed to register otherwise create a token and send the user data back
            try:
                otp.delete()
                member = Member.objects.get(phone=phone_number)

                # Use the FlatMemberSerializer to serialize the member data
                flat_serializer = FlatMemberSerializer(member)

                refresh = RefreshToken.for_user(member)
                return Response(
                    {
                        **flat_serializer.data,  # Include the serialized flattened data
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "existing_user": True,
                    },
                    status=status.HTTP_200_OK,
                )
            except Member.DoesNotExist:
                # If member does not exist, proceed with registration
                return Response(
                    {"existing_user": False},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"detail": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class NICVerificationView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        print(request_data)

        # Perform NIC validation
        nic_valid, message = validate_nic(request_data)
        if not nic_valid:
            return Response(
                {
                    "detail": "Invalid NIC",
                    "reason": message,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"detail": "NIC is valid."},
            status=status.HTTP_200_OK,
        )


class MemberRegistrationView(generics.CreateAPIView):
    serializer_class = MemberSerializer

    def post(self, request, *args, **kwargs):
        request_data = request.data.copy()
        print(request_data)  # Check what data is being sent

        # Use the helper function to nest data
        nested_data = nest_member_data(
            request_data, request.FILES
        )  # Pass request.FILES

        print("The nested data is:", nested_data)

        # Pass the nested data to the serializer for validation and creation
        serializer = self.get_serializer(data=nested_data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()  # Save the member instance
        flat_serializer = FlatMemberSerializer(member)
        refresh = RefreshToken.for_user(member)

        return Response(
            {
                **flat_serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["district"]


class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]


class MembersListView(generics.ListAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]

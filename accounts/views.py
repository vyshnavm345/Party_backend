import random

from rest_framework import generics, status
from rest_framework.response import Response

from .models import OTP, Member
from .serializers import MemberSerializer, OTPSendSerializer, OTPVerifySerializer


class OTPSendView(generics.GenericAPIView):
    serializer_class = OTPSendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp_code = str(random.randint(100000, 999999))  # Generate otp

        # Send OTP to the phone number
        print(f"Sending OTP {otp_code} to {phone_number}")

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
                member = Member.objects.get(phone=phone_number)
                serializer = MemberSerializer(member)
                return Response({"detail": serializer.data}, status=status.HTTP_200_OK)
            except Member.DoesNotExist:
                # If member does not exist, proceed with registration
                return Response(
                    {"detail": "OTP verified. Proceed to register."},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"detail": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class MemberRegistrationView(generics.CreateAPIView):
    serializer_class = MemberSerializer

    def post(self, request, *args, **kwargs):
        # This view will be called after OTP verification
        return super().post(request, *args, **kwargs)

import random

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.edit import FormView
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import UserDeleteForm
from .models import OTP, BaseUser, Candidate, District, Member
from .serializers import (
    CandidateSerializer,
    DistrictSerializer,
    FlatMemberSerializer,
    MemberSerializer,
    OTPSendSerializer,
    OTPVerifySerializer,
)
from .tasks import send_otp_via_textlk
from .utils import nest_member_data, validate_nic

User = get_user_model()


class OTPSendView(generics.GenericAPIView):
    serializer_class = OTPSendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data["phone_number"]
        otp_code = str(random.randint(1000, 9999))

        send_otp_via_textlk(phone_number, otp_code)

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

                # FlatMemberSerializer to serialize the member data
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

        # function for nesting data
        nested_data = nest_member_data(request_data, request.FILES)

        serializer = self.get_serializer(data=nested_data)
        serializer.is_valid(raise_exception=True)
        member = serializer.save()
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
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        queryset = super().get_queryset()
        district_name = self.request.query_params.get("district", None)

        if district_name:
            queryset = queryset.filter(district__name__iexact=district_name)

        return queryset


class CandidateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [AllowAny]


class MembersListView(generics.ListAPIView):
    queryset = Member.objects.select_related("user").all()
    serializer_class = MemberSerializer
    permission_classes = [AllowAny]


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer

    def list(self, request, *args, **kwargs):
        # Override the list method to return only the district names
        districts = District.objects.values_list("name", flat=True).order_by("name")
        return Response({"districts": districts})


class DeleteUserView(FormView):
    form_class = UserDeleteForm
    template_name = "delete_user_form.html"

    def form_valid(self, form):
        contact_info = form.cleaned_data["contact_info"]

        try:
            with transaction.atomic():
                user = (
                    BaseUser.objects.select_related("member")
                    .filter(Q(email=contact_info) | Q(member__phone=contact_info))
                    .first()
                )

                if user:
                    user.delete()
                    return JsonResponse(
                        {
                            "message": f"User with contact info {contact_info} has been deleted."
                        }
                    )

            return JsonResponse(
                {"error": f"No user found with contact info {contact_info}."},
                status=404,
            )

        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    def form_invalid(self, form):
        return JsonResponse({"error": "Invalid form data."}, status=400)

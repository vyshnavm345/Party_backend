from django.urls import path

from .views import (
    CandidateDetailView,
    CandidateListCreateView,
    DistrictListView,
    MemberRegistrationView,
    NICVerificationView,
    OTPSendView,
    OTPVerifyView,
)

urlpatterns = [
    path("send-otp/", OTPSendView.as_view(), name="send-otp"),
    path("verify-otp/", OTPVerifyView.as_view(), name="verify-otp"),
    path("register/", MemberRegistrationView.as_view(), name="register"),
    path("verify-nic/", NICVerificationView.as_view(), name="nic-verification"),
    path(
        "candidates/", CandidateListCreateView.as_view(), name="candidate-list-create"
    ),
    path(
        "candidates/<int:pk>/", CandidateDetailView.as_view(), name="candidate-detail"
    ),
    path("districts/", DistrictListView.as_view(), name="district-list"),
]

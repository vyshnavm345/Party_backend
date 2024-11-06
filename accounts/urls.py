from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CandidateDetailView,
    CandidateListCreateView,
    MemberRegistrationView,
    NICVerificationView,
    OTPSendView,
    OTPVerifyView,
    # DistrictViewSet
    DistrictListView,
)
# router = DefaultRouter()
# router.register(r'districts', DistrictViewSet)

urlpatterns = [
    path("send-otp/", OTPSendView.as_view(), name="send-otp"),
    path("verify-otp/", OTPVerifyView.as_view(), name="verify-otp"),
    path("register/", MemberRegistrationView.as_view(), name="register"),
    path("verify-nic/", NICVerificationView.as_view(), name="nic-verification"),
    path("candidates/", CandidateListCreateView.as_view(), name="candidate-list-create"),
    path("candidates/<int:pk>/", CandidateDetailView.as_view(), name="candidate-detail"),
    path("districts/", DistrictListView.as_view(), name="district-list"),
    # path('', include(router.urls)),
]

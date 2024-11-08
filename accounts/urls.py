from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (  # delete_user_by_email_or_phone,
    CandidateDetailView,
    CandidateListCreateView,
    DeleteUserView,
    DistrictViewSet,
    MemberRegistrationView,
    MembersListView,
    NICVerificationView,
    OTPSendView,
    OTPVerifyView,
)

router = DefaultRouter()
router.register(r"districts", DistrictViewSet)

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
    # path("districts/", DistrictListView.as_view(), name="district-list"),
    path("members/", MembersListView.as_view(), name="members-list"),
    path("delete_user/", DeleteUserView.as_view(), name="delete_user_by_email"),
    path("", include(router.urls)),
]

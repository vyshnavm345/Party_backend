from django.urls import path

from .views import (  # DistrictViewSet
    CandidateDetailView,
    CandidateListCreateView,
    DistrictListView,
    MemberRegistrationView,
    MembersListView,
    NICVerificationView,
    OTPSendView,
    OTPVerifyView,
)

# router = DefaultRouter()
# router.register(r'districts', DistrictViewSet)

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
    path("members/", MembersListView.as_view(), name="members-list"),
    # path('', include(router.urls)),
]

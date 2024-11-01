from django.urls import path

from .views import MemberRegistrationView, OTPSendView, OTPVerifyView, NICVerificationView

urlpatterns = [
    path("send-otp/", OTPSendView.as_view(), name="send-otp"),
    path("verify-otp/", OTPVerifyView.as_view(), name="verify-otp"),
    path("register/", MemberRegistrationView.as_view(), name="register"),
    path('verify-nic/', NICVerificationView.as_view(), name='nic-verification'),
]


# appointment/urls.py
from django.urls import path

from .views import CreateAppointmentView

urlpatterns = [
    path("", CreateAppointmentView.as_view(), name="appointment-create"),
]

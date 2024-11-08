from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment
from .serializers import AppointmentSerializer
from .utils import send_appointment_email


class CreateAppointmentView(APIView):
    def get(self, request):
        appointments = Appointment.objects.all().order_by("-created_at")
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            appointment = serializer.save()
            # Useing helper function to send email (replace with Celery task later)
            # from .tasks import send_appointment_email
            # send_appointment_email.delay(appointment.id)
            send_appointment_email(appointment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import viewsets
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsPatientOrAdmin, CanEditAppointment

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsPatientOrAdmin]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['status', 'doctor__name', 'patient__user__username']  # Adjust these fields as needed
    ordering_fields = ['status', 'date', 'time']
    filterset_fields = ['status', 'date']

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [CanEditAppointment()]
        return super().get_permissions()

    def perform_create(self, serializer):
        try:
            print(f"Creating appointment for user: {self.request.user.username}")
            patient_profile = self.request.user.patient_profile
            serializer.save(patient=patient_profile)
        except AttributeError:
            raise serializers.ValidationError("You must be registered as a patient to book an appointment.")

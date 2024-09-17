from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers, filters
from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsPatientOrAdmin, CanEditAppointment

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsPatientOrAdmin]
    filter_backends = [filters.SearchFilter ,DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'speciality', 'Availability',]
    ordering_fields = ['scheduled','completed','cancelled', 'missed']
    filterset_fields = ['status','date' ]

    

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [CanEditAppointment()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        try:
            # Debugging: Check which user is trying to create an appointment
            print(f"Creating appointment for user: {self.request.user.username}")

            # Ensure the authenticated user has a patient profile
            patient_profile = self.request.user.patient_profile
            serializer.save(patient=patient_profile)
        except AttributeError:
            # Raise a validation error if no patient profile is found
            raise serializers.ValidationError("You must be registered as a patient to book an appointment.")

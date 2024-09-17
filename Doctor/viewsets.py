from rest_framework import viewsets
from .models import Doctor
from .serializers import DoctorSerializer
from .permissions import IsDoctorOrNone

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsDoctorOrNone]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'doctor_from_doctor_app'):
            # Show the logged-in doctor's profile only
            return Doctor.objects.filter(user=user)
        return Doctor.objects.none()  # Return empty queryset for non-doctors

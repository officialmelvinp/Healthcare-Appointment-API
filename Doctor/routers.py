from rest_framework import routers
from .viewsets import DoctorViewSet

app_name = "Doctor"

router = routers.DefaultRouter()
router.register('Doctors', DoctorViewSet)  # Registering the DoctorViewSet with the URL prefix 'Doctors'

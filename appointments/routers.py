# appointments/urls.py

from rest_framework import routers
from .viewsets import AppointmentViewSet

app_name = "appointments"

# Initialize the router
router = routers.DefaultRouter()

# Register the AppointmentViewSet with the URL prefix 'appointments'
router.register('appointments', AppointmentViewSet, basename='appointment')

urlpatterns = router.urls

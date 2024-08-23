from rest_framework import routers #this created after creating a viewset

from .viewsets import UserViewSet, DoctorViewSet, PatientViewSet

app_name = "users"

router = routers.DefaultRouter()
router.register('users',UserViewSet)
router.register('Patients_Profiles', PatientViewSet)
router.register('Doctors_Profiles', DoctorViewSet)




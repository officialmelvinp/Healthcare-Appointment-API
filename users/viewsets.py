from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from .serializers import UserSerializer, PatientProfileSerializer, DoctorsProfileSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly, IsProfileOwnerOrReadOnly,IsPatientProfileOwnerOrReadOnly
from .models import DoctorsProfile, PatientProfile

User = get_user_model()
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserOwnerOrGetAndPostOnly,] #permission to  non user to post and get
    queryset = User.objects.all() #
    serializer_class = UserSerializer
    
    


class DoctorViewSet(viewsets.ModelViewSet #GenericViewSet, #mixins.RetrieveModelMixin, #mixins.UpdateModelMixin, 
                    #  mixins.ListModelMixin,
                    #  mixins.CreateModelMixin,
                    #  mixins.DestroyModelMixin
                     ):
    permission_classes = [IsProfileOwnerOrReadOnly,]
    queryset = DoctorsProfile.objects.all()
    serializer_class = DoctorsProfileSerializer

    
    
class PatientViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                    mixins.DestroyModelMixin
                     ):
    #permission_classes = [IsProfileOwnerOrReadOnly,]
    permission_classes = [IsPatientProfileOwnerOrReadOnly,]
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer


    
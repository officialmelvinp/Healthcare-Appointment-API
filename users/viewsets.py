from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .serializers import UserSerializer, PatientProfileSerializer, DoctorsProfileSerializer
from .permissions import IsUserOwnerOrGetAndPostOnly, IsDoctorOwnerOrReadOnly, IsPatientProfileOwnerOrReadOnly
from .models import DoctorsProfile, PatientProfile
from rest_framework.views import APIView
# from rest_framework import permissions
# from django.contrib.auth import authenticate
# from rest_framework_simplejwt.tokens import AccessToken
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserOwnerOrGetAndPostOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctorOwnerOrReadOnly]
    queryset = DoctorsProfile.objects.all()
    serializer_class = DoctorsProfileSerializer

    def perform_create(self, serializer):
        # Check if a profile already exists for the current user
        user = self.request.user
        if DoctorsProfile.objects.filter(user=user).exists():
            raise ValidationError({"error": "A profile already exists for this user."})
        
        # Save with the current user
        serializer.save(user=user)

    def perform_update(self, serializer):
        # Perform the update operation
        serializer.save()

class PatientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsPatientProfileOwnerOrReadOnly]
    queryset = PatientProfile.objects.all()
    serializer_class = PatientProfileSerializer
    
# @method_decorator(csrf_exempt, name='dispatch')
# class UserLoginView(APIView):
#     permission_classes = [permissions.AllowAny]
    
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         print(username, password)
#         user = authenticate(username=username, password=password)
        
        
#         if user is not None:
#             access_token = AccessToken.for_user(user)
#             return Response({
#                 'access': str(access_token),
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error":"invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        







# from django.contrib.auth import get_user_model
# from rest_framework import viewsets
# from .serializers import UserSerializer, PatientProfileSerializer, DoctorsProfileSerializer
# from .permissions import IsUserOwnerOrGetAndPostOnly, IsDoctorOwnerOrReadOnly, IsPatientProfileOwnerOrReadOnly
# from .models import DoctorsProfile, PatientProfile

# User = get_user_model()

# class UserViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsUserOwnerOrGetAndPostOnly]
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

# class DoctorViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsDoctorOwnerOrReadOnly]
#     queryset = DoctorsProfile.objects.all()
#     serializer_class = DoctorsProfileSerializer

#     def perform_create(self, serializer):
#         # Save with the current user if necessary
#         serializer.save(user=self.request.user)

#     def perform_update(self, serializer):
#         # Perform the update operation
#         serializer.save()

# class PatientViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsPatientProfileOwnerOrReadOnly]
#     queryset = PatientProfile.objects.all()
#     serializer_class = PatientProfileSerializer

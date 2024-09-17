from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import DoctorsProfile, PatientProfile

User = get_user_model()

class DoctorsProfileSerializer(serializers.ModelSerializer):
    specialization_display = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)  # Accessing username from related User model

    class Meta:
        model = DoctorsProfile
        fields = ['url', 'username', 'id', 'specialization', 'image', 'specialization_display']

    def get_specialization_display(self, obj):
        return obj.get_specialization_display()

class PatientProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Accessing username from related User model

    class Meta:
        model = PatientProfile
        fields = ['url', 'username', 'id', 'date_of_birth', 'image']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(
        read_only=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    doctor_profile = DoctorsProfileSerializer(read_only=True, source='doctors_profile_from_users')
    patient_profile = PatientProfileSerializer(read_only=True)
    specialization = serializers.ChoiceField(choices=DoctorsProfile.SPECIALIZATION_CHOICES, write_only=True, required=False)
    date_of_birth = serializers.DateField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'url', 'id', 'username', 'email', 'first_name', 'last_name', 
            'password', 'old_password', 'is_patient', 'is_doctor', 
            'doctor_profile', 'patient_profile', 'date_of_birth', 'specialization'
        ]

    def validate(self, data):
        request = self.context.get('request')
        request_method = request.method if request else None
        password = data.get('password')
        first_name = data.get('first_name')
        password = data.get('password')
        is_patient = data.get('is_patient', False)
        is_doctor = data.get('is_doctor', False)
        email = data.get("email")

        if request_method == 'POST':
            if not password:
                raise serializers.ValidationError({"info": "Please provide a password."})
            if not first_name:
                raise serializers.ValidationError({"info": "First name is required."})
            # if not password:
            #     raise serializers.ValidationError({"info": "Please provide a password."})
            if is_patient and is_doctor:
                raise serializers.ValidationError("A user cannot be both a patient and a doctor.")
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already exist.")
                
        elif request_method in ['PUT', 'PATCH']:
            old_password = data.get('old_password')
            if password and not old_password:
                raise serializers.ValidationError({'info': "Please provide the old password if you want to update the password."})
            if is_patient and is_doctor:
                raise serializers.ValidationError("A user cannot be both a patient and a doctor.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        is_doctor = validated_data.pop('is_doctor', False)
        is_patient = validated_data.pop('is_patient', False)
        specialization = validated_data.pop('specialization', None)
        date_of_birth = validated_data.pop('date_of_birth', None)

        user = User(**validated_data)
        user.set_password(password)
        user.is_patient = is_patient
        user.is_doctor = is_doctor
        user.save()

        # Create profiles based on user roles
        if is_doctor:
            profile, _ = DoctorsProfile.objects.get_or_create(user=user)
            if specialization:
                profile.specialization = specialization
                profile.save()

        if is_patient:
            patient_profile, _ = PatientProfile.objects.get_or_create(user=user)
            if date_of_birth:
                patient_profile.date_of_birth = date_of_birth
                patient_profile.save()

        return user

    def update(self, instance, validated_data):
        user = instance

        # Handle password change
        if 'password' in validated_data:
            password = validated_data.pop('password')
            old_password = self.initial_data.get('old_password', None)
            if old_password and user.check_password(old_password):
                user.set_password(password)
            else:
                raise serializers.ValidationError({"info": "Old password is incorrect."})
        
        # Update user attributes
        for attr, value in validated_data.items():
            setattr(user, attr, value)

        user.save()

        # Update or delete doctor's profile
        if user.is_doctor:
            profile, _ = DoctorsProfile.objects.get_or_create(user=user)
            specialization = validated_data.get('specialization', None)
            if specialization:
                profile.specialization = specialization
                profile.save()
        else:
            DoctorsProfile.objects.filter(user=user).delete()
        
        # Update or delete patient's profile
        if user.is_patient:
            patient_profile, _ = PatientProfile.objects.get_or_create(user=user)
            date_of_birth = validated_data.get('date_of_birth', None)
            if date_of_birth:
                patient_profile.date_of_birth = date_of_birth
                patient_profile.save()
        else:
            PatientProfile.objects.filter(user=user).delete()

        return user

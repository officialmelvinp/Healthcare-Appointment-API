from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from .models import DoctorsProfile, PatientProfile

User = get_user_model()

class DoctorsProfileSerializer(serializers.ModelSerializer):
    #user = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    class Meta:
        model = DoctorsProfile
        fields = ['url', 'id', 'specialization', 'image']

class PatientProfileSerializer(serializers.ModelSerializer):
    #user = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='user-detail')
    class Meta:
        model = PatientProfile
        fields = ['url', 'id', 'date_of_birth', 'image']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    doctor_profile = DoctorsProfileSerializer(read_only=True, source='doctorsprofile')
    patient_profile = PatientProfileSerializer(read_only=True, source='patientprofile')

    class Meta:
        model = User
        fields = ['url',
            'id', 'username', 'email', 'first_name', 'last_name', 
            'password', 'old_password', 'is_patient', 'is_doctor', 
            'doctor_profile', 'patient_profile'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'old_password': {'write_only': True},
            'username': {'read_only': True},
        }

    def validate(self, data):
        request = self.context.get('request')# To check if the request is a POST, PUT, or PATCH
        request_method = request.method if request else None
        password = data.get('password') # To check if a password is given and get it

        is_patient = data.get('is_patient', False)
        is_doctor = data.get('is_doctor', False)
        
        if request_method == 'POST':
            if not password:
                raise serializers.ValidationError({"info": "Please provide a password."})
            if is_patient and is_doctor:
                raise serializers.ValidationError("A user cannot be both a patient and a doctor.")
        
        elif request_method in ['PUT', 'PATCH']:
            old_password = data.get('old_password')
            if password and not old_password:
                raise serializers.ValidationError({'info': "Please provide the old password if you want to update the password."})
            if is_patient and is_doctor:
                raise serializers.ValidationError("A user cannot be both a patient and a doctor.")

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        try:
            user = instance
            if 'password' in validated_data:
                password = validated_data.pop('password')
                old_password = validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise Exception("Old password is incorrect.")
                user.save()
                return user
        except Exception as err:
            raise serializers.ValidationError({"info": err})
        return super(UserSerializer, self).update(instance, validated_data)


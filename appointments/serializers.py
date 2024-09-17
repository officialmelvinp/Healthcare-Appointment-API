# serializers.py

from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient_username = serializers.SerializerMethodField() # Accessing username from related appointment model
    class Meta:
        model = Appointment
        fields = ['url', 'id', 'patient_username', 'patient', 'doctor', 'date', 'time', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at',
                            'status',]
        
        
    def get_patient_username(self, obj):
        # Return the username of the patient associated with the appointment
        return obj.patient.user.username if obj.patient and obj.patient.user else None


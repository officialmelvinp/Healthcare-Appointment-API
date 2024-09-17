# serializers.py

from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    patient_username = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ['url', 'id', 'patient_username', 'patient', 'doctor', 'date', 'time', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']  # Remove 'status' from read_only_fields if it should be writable

    def get_patient_username(self, obj):
        return obj.patient.user.username if obj.patient and obj.patient.user else None

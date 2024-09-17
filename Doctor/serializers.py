from rest_framework import serializers
from .models import Doctor

class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    specialization_display = serializers.SerializerMethodField()
    username = serializers.CharField(source='user.username', read_only=True)  # Accessing username from related User model

    class Meta:
        model = Doctor
        fields = ['url', 'id', 'user', 'username', 'name', 'specialization', 'availability', 'specialization_display']

    def get_specialization_display(self, obj):
        return obj.get_specialization_display()

from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Doctor(models.Model):
    SPECIALIZATION_CHOICES = [
        ('GP', 'General Practitioner'),
        ('CARD', 'Cardiologist'),
        ('DERM', 'Dermatologist'),
        ('ORTH', 'Orthopedic'),
        ('NEUR', 'Neurologist'),
        ('DENT', 'Dental'),
        # Ensure these values are what you intend to use and are unique
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_from_doctor_app')  # Updated related_name
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=5, choices=SPECIALIZATION_CHOICES)  # Ensure max_length matches the longest choice key
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.get_specialization_display()}"

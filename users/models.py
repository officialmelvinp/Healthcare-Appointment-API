import os
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.deconstruct import deconstructible

# Utility class for generating profile image paths
@deconstructible
class GenerateProfileImagePath:
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.id}/images/'  # Generates path based on the user ID
        name = f'profile_image.{ext}'
        return os.path.join(path, name)

user_profile_image_path = GenerateProfileImagePath()

# Custom User model
class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

    # Overrides default group and permission related names to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )

    def __str__(self):
        return self.username

# DoctorsProfile model linked to the custom User model
class DoctorsProfile(models.Model):
    SPECIALIZATION_CHOICES = [
        ('GP', 'General Practitioner'),
        ('CARD', 'Cardiologist'),
        ('DERM', 'Dermatologist'),
        ('ORTH', 'Orthopedic'),
        ('NEUR', 'Neurologist'),
        ('DENT', 'Dental'),
        # Add more specializations as required
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='doctors_profile'  # Changed related_name for clarity
    )
    image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES, blank=True)
    # Ensure the specialization field is optional with blank=True if not mandatory

    def __str__(self):
        return f'{self.user.username} (Doctor)'

# PatientProfile model linked to the custom User model
class PatientProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} (Patient)'

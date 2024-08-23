# models.py
import os
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateProfileImagePath(object):
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/accounts/{instance.id}/images/'  # Use instance.id instead of instance.user.id
        name = f'profile_image.{ext}'
        return os.path.join(path, name)

user_profile_image_path = GenerateProfileImagePath()

class User(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)

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

class DoctorsProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)
    specialization = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.user.username} (Doctor)'

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to=user_profile_image_path, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} (Patient)'

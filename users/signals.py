from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import PatientProfile, DoctorsProfile
from Doctor.models import Doctor

User = get_user_model()

@receiver(post_save, sender=User)
def handle_user_profiles(sender, instance, created, **kwargs):
    """
    Create or update user profiles based on user role when a User is created or updated.
    """
    if created:
        if instance.is_patient:
            PatientProfile.objects.get_or_create(user=instance)
            print("PatientProfile created.")
        if instance.is_doctor:
            DoctorsProfile.objects.get_or_create(user=instance)
            print("DoctorsProfile created.")
            # Create or update Doctor profile
            Doctor.objects.get_or_create(user=instance, defaults={'name': instance.username})
            print("Doctor profile created or updated.")
    else:
        # Handle updates to existing profiles
        if instance.is_patient:
            patient_profile, _ = PatientProfile.objects.get_or_create(user=instance)
            patient_profile.save()
        if instance.is_doctor:
            doctors_profile, _ = DoctorsProfile.objects.get_or_create(user=instance)
            doctors_profile.save()
            # Update Doctor profile
            Doctor.objects.update_or_create(user=instance, defaults={'name': instance.username})
            print("Doctor profile updated.")

@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    """
    Automatically set a unique username based on the user's first and last name if not provided.
    """
    if not instance.username:
        base_username = f'{instance.first_name}_{instance.last_name}'.lower()
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base_username}_{counter}'
            counter += 1
        instance.username = username

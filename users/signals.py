# #signal file is created or can be created to generate or create user automatically and get notifications.

# signals.py
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import PatientProfile, DoctorsProfile





User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_patient:
            PatientProfile.objects.create(user=instance)
        elif instance.is_doctor:
            DoctorsProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_patient and hasattr(instance, 'patientprofile'):
        instance.patientprofile.save()
    elif instance.is_doctor and hasattr(instance, 'doctorsprofile'):
        instance.doctorsprofile.save()

@receiver(pre_save, sender=User)
def set_username(sender, instance, **kwargs):
    if not instance.username:
        base_username = f'{instance.first_name}_{instance.last_name}'.lower()
        username = base_username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f'{base_username}_{counter}'
            counter += 1
        instance.username = username








# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver
# from django.contrib.auth import get_user_model
# from .models import PatientProfile, DoctorsProfile

# User = get_user_model()

# @receiver(pre_save, sender=User)
# def set_username(sender, instance, **kwargs): #automating username generation to avoid where users have the same user name
#     if not instance.username:
#         base_username = f'{instance.first_name}_{instance.last_name}'.lower()
#         username = base_username
#         counter = 1
#         while User.objects.filter(username=username).exists():
#             username = f'{base_username}_{counter}'
#             counter += 1
#         instance.username = username

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_patient:
#             PatientProfile.objects.create(user=instance)
#         elif instance.is_doctor:
#             DoctorsProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.is_patient and hasattr(instance, 'patientprofile'):
#         instance.patientprofile.save()
#     elif instance.is_doctor and hasattr(instance, 'doctorsprofile'):
#         instance.doctorsprofile.save()


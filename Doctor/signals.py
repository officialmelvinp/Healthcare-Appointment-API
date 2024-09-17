# Doctor/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Doctor

User = get_user_model()

@receiver(post_save, sender=Doctor)
def create_or_update_doctor_profile(sender, instance, created, **kwargs):
    if created:
        # If Doctor instance is created, you might want to do something
        print(f"Doctor created: {instance.name} with specialization {instance.get_specialization_display()}")
    else:
        # Update logic if necessary
        print(f"Doctor updated: {instance.name} with specialization {instance.get_specialization_display()}")

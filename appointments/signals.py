from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Appointment
from django.core.mail import send_mail

@receiver(post_save, sender=Appointment)
def appointment_created_or_updated(sender, instance, created, **kwargs):
    if instance.patient and instance.patient.user and instance.patient.user.email:
        if created:
            send_mail(
                subject='New Appointment Scheduled',
                message=f'An appointment has been scheduled with {instance.doctor} on {instance.date} at {instance.time}.',
                from_email='noreply@yourdomain.com',
                recipient_list=[instance.patient.user.email],
                fail_silently=False,
            )
            print(f"Appointment created: {instance}")
        else:
            send_mail(
                subject='Appointment Updated',
                message=f'Your appointment with {instance.doctor} has been updated to {instance.date} at {instance.time}.',
                from_email='noreply@yourdomain.com',
                recipient_list=[instance.patient.user.email],
                fail_silently=False,
            )
            print(f"Appointment updated: {instance}")
    else:
        print(f"Appointment notification failed due to missing user or email: {instance}")

@receiver(post_delete, sender=Appointment)
def appointment_deleted(sender, instance, **kwargs):
    if instance.patient and instance.patient.user and instance.patient.user.email:
        send_mail(
            subject='Appointment Canceled',
            message=f'Your appointment with {instance.doctor} on {instance.date} at {instance.time} has been canceled.',
            from_email='noreply@yourdomain.com',
            recipient_list=[instance.patient.user.email],
            fail_silently=False,
        )
        print(f"Appointment deleted: {instance}")
    else:
        print(f"Appointment deletion notification failed due to missing user or email: {instance}")

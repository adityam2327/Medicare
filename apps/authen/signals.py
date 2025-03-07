from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from apps.doctor.models import DoctorProfile
from apps.patient.models import PatientProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:  # Assuming doctors are staff users
            DoctorProfile.objects.create(user=instance)
        else:
            PatientProfile.objects.create(user=instance)
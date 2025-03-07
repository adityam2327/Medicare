from django.db import models
from django.contrib.auth.models import User

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=255, default="General")
    hospital = models.CharField(max_length=255, default="Unknown Hospital")  # Default value added
    experience = models.IntegerField(default=0)  # Default value added
    contact_number = models.CharField(max_length=15, blank=True, null=True)  # Make it optional
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


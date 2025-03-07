from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Rescheduled', 'Rescheduled'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='patient_appointments'
    )
    doctor_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    appointment_type = models.CharField(max_length=100)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Scheduled')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor_name} - {self.date} at {self.time} ({self.status})"

    class Meta:
        ordering = ['date', 'time']

class Hospital(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class CommunityUpdate(models.Model):
    CATEGORY_CHOICES = [
        ('Health', 'Health'),
        ('Events', 'Events'),
        ('Alerts', 'Alerts'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Health')
    content = models.TextField()
    image = models.ImageField(upload_to='community_updates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class HealthcareProfessional(models.Model):
    SPECIALIZATION_CHOICES = [
        ('General Physician', 'General Physician'),
        ('Cardiologist', 'Cardiologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Psychologist', 'Psychologist'),
    ]

    name = models.CharField(max_length=200)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    contact_info = models.CharField(max_length=100)
    experience = models.PositiveIntegerField(help_text="Years of experience")
    availability = models.BooleanField(default=True)
    profile_image = models.ImageField(upload_to='healthcare_profiles/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.specialization}"

class MedicalInfo(models.Model):
    CATEGORY_CHOICES = [
        ('General Health', 'General Health'),
        ('Fitness', 'Fitness'),
        ('Diet', 'Diet'),
        ('Mental Health', 'Mental Health'),
        ('Diseases', 'Diseases'),
         ('Medicine', 'Medicine'),
        ('Equipment', 'Equipment'),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    content = models.TextField()
    image = models.ImageField(upload_to='medinfo_images/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='patient_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

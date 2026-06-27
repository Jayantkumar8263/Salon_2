from django.db import models
from salon_app.models import StaffAttendance, StaffProfile, WorkingHours
from django.contrib.auth.models import User
# Create your models here.

# __profile__
class owner_profile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

# __salon settings__
class SalonSettings(models.Model):
    salon_name = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.salon_name
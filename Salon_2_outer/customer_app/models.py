from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# ___Customer profile Model___ 
   
class CustomerProfile(models.Model):
    """ The customer who want to login in salon app and book an appointment. """
    user  = models.OneToOneField(User, on_delete=models.CASCADE, related_name= 'customer_profile')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    banner = models.ImageField(upload_to='banners/', blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.user.get_full_name()

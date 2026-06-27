from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

#___Staff profile model_____
class StaffProfile(models.Model):
    '''staff profile who are working in slaon, who can login '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null= True, blank=True)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    Service = models.ManyToManyField('salon_app.Service', related_name='staff_members')# one staff member can provide multiple sevices the customer so that is why we are using many-many feads 
    bio = models.TextField(blank=True, null=True)
    experience_years = models.IntegerField(blank=True, null=True)
    def __str__(self):
        if self.user:
            return self.user.username # we will get the name of the person or staff
        return "Not a member of our staff" 
    
    def is_on_duty_now(self):# IT will check for the staff is active or not in the current date and time. 
        try:
            now = timezone.now() # to get the current day and time
            day = now.weekday()# Current day of the week as an integer, where Monday is 0 and Sunday is 6.
            current_time = now.time()
            
            # Checking if a matching schedule exists
            # this looks for a WorkingHours entry for the staff member where the current day matches, and the current time is between their start and end time.
            is_working = self.working_hours.filter(day_of_week = day, start_time = current_time, end_time = current_time).exists() # .exists() is fast, it just returns True or False 
            return is_working
        except Exception:# If anything goes wrong it will return false.
            return False
    
#___ staff details model___
class StaffDetails(models.Model):
    staff = models.OneToOneField(StaffProfile, on_delete=models.CASCADE, related_name='details')
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='staff_photos/', blank=True, null=True)
    def __str__(self):
        return f"Details of {self.staff.user.get_full_name()}"

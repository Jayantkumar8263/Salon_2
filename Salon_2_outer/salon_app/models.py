from django.db import models
from django.utils import timezone 
from datetime import timedelta
from django.core.exceptions import ValidationError
from customer_app.models import CustomerProfile
from Staff_app.models import StaffProfile
# Create your models here.

# ___Service we provide__
class Service(models.Model):
    ''' The services we want to provide in the salon '''
    service_name = models.CharField(max_length=50)
    description = models.TextField(null= True, blank= True)
    duration = models.IntegerField(help_text= "in minutes")# for time we should always use intiger feald, it can count time in minutes. 
    price = models.DecimalField(max_digits = 8, decimal_places = 2) #for price we are using decimal feald for conting money.
    is_active = models.BooleanField(default = True)
    def __str__(self):
        return f"{self.service_name} - ${self.price}" # it will show the service name and the price of the service in admin pannel as well as.
    

# __ Appointment model__ 

class Appointment(models.Model):
    # To book a single appointment for the customer with staff member for a particular service at a specific date and time. 
    appointment_date = models.DateTimeField()
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='customer_appointments', null= True)
    # on_delete=models.CASCADE : the database automatically finds and deletes all Appointment records of the customer 
    #related_name='customer_appointments: related_name is simply a way to give this reverse relationship, we are calling the customerprofile in the appointments by using related name.
    #for connecting two coloums/models we are using foreign key
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='Staff_appointments', null = True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null = True) 
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ('No-show', 'No-show'),
    ]
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='Pending')
    start_time = models.DateTimeField()
    booked_at = models.DateField(auto_now_add = True)
    def __str__(self):
        return f"{self.customer.user.get_full_name()} - {self.service.service_name} on {self.appointment_date}"
    #End time 
    def end_time(self):
        return self.appointment_date + timedelta(minutes=self.service.duration)# it will add the duration of the service to the appointment date and time to calculate the end time of the appointment.
    #clean method for validation
    def clean(self):
        super().clean()# here i am calling the parent class's clean method to ensure that any validation logic defined in the parent class is also executed.
        if self.start_time and self.start_time < timezone.now():
            raise ValidationError({'start_time': 'Appointment cannot be in the past'})
        if self.staff and self.service: # this if statement the condition is applied for staff and srevices 
            if self.service not in self.staff.Service.all():# In in this if staff does'nt or can't perform that service it will rise validation error, this.staff.Service.all() gets all the services that the staff member can perform.
                raise ValidationError({'staff': f'{self.staff.user.get_full_name()} does not perform {self.service.service_name}'})
        if self.appointment_date and self.service:
            if self.service not in self.staff.Service.all():
                raise ValidationError(
                    {'staff': f'{self.staff.user.get_full_name()} does not perform {self.service.service_name}'})

#____ Payment Model___

class Payment(models.Model):
    '''to show payment status and to make payment options.'''
    STATUS_CHOICES = [   # for showing current status
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
        #('Refunded', 'Refunded'), if there is a refound policy 
        ]
        
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name= 'payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length = 50, choices = STATUS_CHOICES, default = 'Pending')
    payment_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return f"Payment of ${self.amount} for {self.appointment.id} - Status: {self.status}"

#___ Working Hours Model____

class WorkingHours(models.Model): # for showing the status of the staff is he working or not 
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name="working_hours")
    day_of_week = models.IntegerField(choices = DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    class Meta: # in this line i am using Meta class to define some additional properties for the WorkingHours model, such as unique constraints and default ordering.
        unique_together = ('staff', 'day_of_week') # i used unique_together variable to ensure that each staff member can have only one set of working hours per day of the week.
        ordering = ['staff', 'day_of_week']# this will order the working hours first by staff member and then by day of the week.

    def __str__(self):
        # This will now work!
        return f"{self.staff.user.first_name} - {self.get_day_of_week_display()}: {self.start_time} - {self.end_time}" # it will show the staff name with their working hours in the admin pannel.
    
#___ Staff Attendance Model____

class StaffAttendance(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10,
        choices=(
            ("Present", "Present"),
            ("Absent", "Absent"),
            ("Leave", "Leave"), 
            ),
        default="Present",
    )

    class Meta: # in this line i am using Meta class to define some additional properties for the StaffAttendance model, such as default ordering.
        ordering = ["-date"] # it will order the attendance records by date in descending order, so the most recent records appear first.

    def __str__(self):
        return f"{self.staff.user.username} - {self.date} - {self.status}"

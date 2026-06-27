# we made this file to convert moddels to json format for api purpose

# imports 
from rest_framework import serializers
from salon_app.models import Service, Appointment, WorkingHours

# for Service model
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'service_name', 'price', 'duration']
        
# for Appointment model
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        
# for WorkingHours model
class WorkingHoursSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.user.get_full_name', read_only=True)
    
    class Meta:
        model = WorkingHours
        fields = ['id', 'staff', 'staff_name', 'day_of_week', 'start_time', 'end_time']


from rest_framework import serializers
from django.contrib.auth.models import User
from salon_app.serializers import ServiceSerializer
from customer_app.serializers import UserSerializer
from .models import StaffProfile

# Staff Profile Serializer
class StaffProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True) # here we are using the user serilizer from customer app to get the user details
    services = serializers.SerializerMethodField() # here SerializerMethodField() is used to get the services provided by the staff member, it basically calls the get_services method to fetch the services
    class Meta:
        model = StaffProfile
        fields = ['id', 'user', 'photo', 'phone_number', 'services', 'bio', 'experience_years']
        
    def get_services(self, obj):
        services = obj.services.all()
        return ServiceSerializer(services, many=True).data 
    # here we are using the ServiceSerializer to serialize the services provided by the staff member, (services, many=True) means that we are serializing multiple service objects and storing it in the jason format, .data is used to get the serialized data in json format
    
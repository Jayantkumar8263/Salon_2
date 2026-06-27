from customer_app.models import CustomerProfile
from rest_framework import serializers
from django.contrib.auth.models import User

# for CustomerProfile model
class CustomerProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = CustomerProfile
        fields = ['id', 'user', 'user_name', 'email', 'bio', 'phone_number', 'banner', 'avatar']

# for user

class UserSerializer(serializers.ModelSerializer):
    customer_profile = CustomerProfileSerializer(read_only=True)
    class Meta: 
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
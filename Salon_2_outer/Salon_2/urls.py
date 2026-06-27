"""
URL configuration for Salon_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as auth_views

# Import ViewSets
from salon_app.views import ServiceViewSet, AppointmentViewSet
from customer_app.views import CustomerProfileViewSet
from Staff_app.views import StaffProfileViewSet

# Router setup
router = DefaultRouter()
router.register(r'api/services', ServiceViewSet)
router.register(r'api/appointments', AppointmentViewSet, basename='appointment')
router.register(r'api/profiles/customer', CustomerProfileViewSet, basename='customer-profile')
router.register(r'api/profiles/staff', StaffProfileViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('salon_app.urls')),
    path('', include('owner.urls')),
    path('', include('customer_app.urls')),
    path('', include('Staff_app.urls')),
    
     # API Routes
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', auth_views.obtain_auth_token),  # Token authentication
]
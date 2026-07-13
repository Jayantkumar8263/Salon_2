from django.shortcuts import render
from .models import Service, WorkingHours
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Service, Appointment
from .serializers import ServiceSerializer, AppointmentSerializer
# Home page
def home(request):
    services = Service.objects.all()[:3]
    context = {"services": services}
    return render(request, "generals/home.html", context)

# All services list
def service_list(request):
    services = Service.objects.all()
    return render(request,"service_list.html",{"services": services})

# Public working hours page (optional)
def workinghours_view(request):
    working_hours = WorkingHours.objects.all()
    return render(request, "working_hours.html", {"working_hours": working_hours})

# __ Service and Appointment ViewSets for API __ #
class ServiceViewSet(viewsets.ModelViewSet): # this class is created to handle Service model API(Application Programming Interface.) requests
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer # Serializer for Service model
    permission_classes = [AllowAny]  # Public access
    


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all().order_by("id")
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        print("GET_QUERYSET CALLED")
        print("request.user =", user)

        if user.is_superuser:
            print("superuser queryset")
            return Appointment.objects.all().order_by("id")

        if hasattr(user, "customer_profile"):
            print("customer profile id =", user.customer_profile.id)
            return Appointment.objects.filter(customer__user=user).order_by("id")

        if hasattr(user, "staff_profile"):
            print("staff profile id =", user.staff_profile.id)
            return Appointment.objects.filter(staff__user=user).order_by("id")

        print("no matching profile")
        return Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        print("CUSTOM CREATE CALLED")
        print("request.user =", request.user)
        print("has customer_profile =", hasattr(request.user, "customer_profile"))

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if hasattr(request.user, "customer_profile"):
            print("saving with customer profile id =", request.user.customer_profile.id)
            instance = serializer.save(customer=request.user.customer_profile)
        else:
            print("saving without customer profile")
            instance = serializer.save()

        output_serializer = self.get_serializer(instance)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        
        
    @action(detail=True, methods=['post'])# action is a decorator which is used for defining custom actions on viewsets, custom actions means ki hum apne hisab se koi bhi method\ bana sakte hai(get/post/put/delete) by which we can perform specific operations on the model instances, , viwewset means ki hum ek hi jagah par multiple related views ko manage kar sakte  hai jaise ki views.py, here detail=True ka matlab hai ki ye action specific appointment instance par operate karega, methods=['post'] ka matlab hai ki ye action sirf POST request ke liye accessible hoga
    def cancel(self, request, pk = None): # this function is used for cancelling the appointment.
        appointment = self.get_object()# this method retrieves the specific appointment instance based on the primary key (pk) provided in the URL.
        appointment.status = 'Cancelled'
        appointment.save()
        return Response({"message": "Appointment cancelled successfully"})
    
    
    
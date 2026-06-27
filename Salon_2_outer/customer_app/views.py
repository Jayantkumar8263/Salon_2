from datetime import timedelta
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin import AdminSite
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from salon_app.models import Appointment, Service
from salon_app.forms import AppointmentForm
from .models import CustomerProfile
from .forms import CustomRegistrationForm, ProfileUpdateForm, CustomerProfileUpdateForm, CustomerSign_upForm
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CustomerProfile
from .serializers import CustomerProfileSerializer
# ---------- AUTH / REGISTRATION ----------

def registration(request): # this view is for registration of the users or the customers 
    if request.method == "POST": # here we created 
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomerProfile.objects.get_or_create(user=user)
            messages.success(request, "Your account has been created successfully.")
            return redirect("home")
    else:
        form = CustomRegistrationForm()
    return render(request, "registration.html", {"form": form})



def signup_view(request):
    if request.method == "POST":
        form = CustomerSign_upForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = CustomerSign_upForm()
    return render(request, "signup.html", {"form": form})


def u_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        messages.error(request, "Invalid username or password")
    return render(request, "signup.html")


def signin_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile")
        messages.error(request, "Invalid username or password")
    return render(request, "signin.html")


def u_logout(request):
    logout(request)
    return redirect("home")


def admin_view(request):
    admin_site = AdminSite()
    return render(request, "admin.html", {"admin_site": admin_site})

# ---------- PROFILE ----------

@login_required
def u_profile(request):
    user = request.user
    customer_profile, created = CustomerProfile.objects.get_or_create(user=user)

    now = timezone.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

    upcoming_appointments = (
        Appointment.objects.filter(
            customer=customer_profile,
            start_time__gte=today_start,
        )
        .exclude(status="Cancelled")
        .order_by("start_time")
    )

    context = {
        "user": user,
        "upcoming_appointments": upcoming_appointments,
    }
    return render(request, "profile/profile.html", context)



@login_required
def profile_edit(request):
    user = request.user
    customer_profile, created = CustomerProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = ProfileUpdateForm(request.POST, instance=user)
        profile_form = CustomerProfileUpdateForm(
            request.POST,
            request.FILES,         
            instance=customer_profile,
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()    # porfille banner and the edits are going to be saved here 
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
    else:
        user_form = ProfileUpdateForm(instance=user) 
        profile_form = CustomerProfileUpdateForm(instance=customer_profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "profile/profile_edit.html", context)


# ---------- APPOINTMENTS ----------

@login_required
def create_appointment(request):
    try:
        customer_profile = request.user.customer_profile
    except CustomerProfile.DoesNotExist:
        messages.error(request, "You need a customer profile to book an appointment.")
        return redirect("appointment_list")

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = customer_profile
            try:
                appointment.full_clean()
            except Exception:
                form.add_error(None, "Double booking detected or invalid input.")
                return render(request, "appointment_form.html", {"form": form})
            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect("appointment_list")
        return render(request, "appointment_form.html", {"form": form})

    form = AppointmentForm()
    return render(request, "appointment_form.html", {"form": form})


@login_required
def appointmentform_view(request):
    customer_profile = get_object_or_404(CustomerProfile, user=request.user)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = customer_profile
            if appointment.start_time:
                appointment.appointment_date = appointment.start_time
            if appointment.service and appointment.service.duration:
                minutes = appointment.service.duration
            else:
                minutes = 20
            appointment.end_time = appointment.start_time + timedelta(minutes=minutes)
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return redirect("appointment_list")
    else:
        form = AppointmentForm()
    return render(request, "appointment/appointment_form.html", {"form": form})


@login_required
def appointment_book_service(request, service_id):
    customer_profile = get_object_or_404(CustomerProfile, user=request.user)
    service = get_object_or_404(Service, pk=service_id)

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = customer_profile
            appointment.service = service
            appointment.appointment_date = appointment.start_time
            minutes = appointment.service.duration or 20
            appointment.end_time = appointment.start_time + timedelta(minutes=minutes)
            appointment.save()
            messages.success(request, "Appointment booked successfully.")
            return redirect("appointment_list")
    else:
        form = AppointmentForm(initial={"service": service})
    return render(
        request,
        "appointment/appointment_form.html",
        {"form": form, "service": service},
    )


@login_required
def appointmentlist_View(request):
    customer_profile = get_object_or_404(CustomerProfile, user=request.user)
    appointments = Appointment.objects.filter(customer=customer_profile).order_by(
        "-start_time"
    )
    return render(
        request,
        "appointment/appointment_list.html",
        {"appointments": appointments},
    )


@login_required
def appointmentdetail_view(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    return render(
        request,
        "appointment/appointment_detail.html",
        {"appointment": appointment},
    )


@login_required
def appointment_detail(request, pk):
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        customer=request.user.customer_profile,
    )
    return render(request, "appointment_detail.html", {"appointment": appointment})


@login_required
def appointment_edit(request, pk):
    customer_profile = get_object_or_404(CustomerProfile, user=request.user)
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        customer_id=customer_profile.id,
    )

    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = customer_profile
            obj.end_time = obj.start_time + timedelta(minutes=obj.service.duration)
            obj.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect("appointment_list")
    else:
        form = AppointmentForm(instance=appointment)

    return render(
        request,
        "appointment/appointment_form.html",
        {"form": form, "appointment": appointment},
    )


@login_required
def appointment_cancle(request, pk):
    customer_profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )
    appointment = get_object_or_404(
        Appointment,
        pk=pk,
        customer_id=customer_profile.id,
    )
    if request.method == "POST":
        appointment.status = "Cancelled"
        appointment.save()
        appointment.delete()
        messages.success(request, "Appointment cancelled successfully.")
        return redirect("appointment_list")
    return render(
        request,
        "appointment/appointment_confirm_delete.html",
        {"appointment": appointment},
    )

class CustomerProfileViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['get'])# here we are using get method so that user do not have to login again and again. action decorator use kar rahe hain kyoki ye hume ek custom action provide karta hai jo humare viewset mein add hota hai, custom actions matlab ki hum apne viewset mein extra functionality add kar sakte hain jo standard CRUD operations se alag hoti hai.
    def profile(self, request):# here in this function self use kar rehe hai kyoki ye class ka part hai aur request humare paas user ka sara data leke aata hai.
        profile = CustomerProfile.objects.get_or_create(user=request.user)# ye line check karti hai ki kya user ka profile already exist karta hai ya nahi, agar nahi karta to naya profile create kar deti hai.
        serializer = CustomerProfileSerializer(profile[0])# ye line profile ko serialize karti hai taaki usse JSON format mein convert kiya ja sake jo API responses ke liye suitable hota hai.
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])# put method is used for updating existing resources, detail = false means user ko detail dalne ki zarurat nahi hai kyoki hum apne khud ke profile ko update kar rahe hain.
    def update_profile(self, request):
        profile = request.user.customer_profile# ye line user ke profile ko access karti hai jo ki request ke through milta hai, isse hum current logged in user ke profile ko update kar sakte hain.
        serilizer = CustomerProfileSerializer(profile, data=request.data, partial=True)# ye line profile ko update karne ke liye serializer ka use karti hai, partial = true ka matlab hai ki hum sirf kuch fields ko hi update kar sakte hain bina poore object ko replace kiye.
        if serilizer.is_valid():# ye line check karti hai ki jo data humne provide kiya hai wo valid hai ya nahi, agar valid hai to hum profile ko save kar dete hain.
            serilizer.save()
            return Response(serilizer.data)# it returns the updated profile data in the response.
        return Response(serilizer.errors, status=status.HTTP_400_BAD_REQUEST)# this line returns any validation errors if the provided data is not valid, along with a 400 Bad Request status code.
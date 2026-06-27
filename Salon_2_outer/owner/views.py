from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import owner_profile, SalonSettings
from Staff_app.models import StaffProfile
from salon_app.models import StaffAttendance
from django.shortcuts import redirect
from django.utils import timezone
from customer_app.forms import CustomRegistrationForm
from django.contrib import messages
# Create your views here.

@login_required
def salon_settings_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only salon admin can access this page.")

    settings = SalonSettings.objects.first()

    if request.method == "POST":
        if settings: # if a SalonSettings object already exists
            # update
            settings.salon_name = request.POST.get("salon_name", settings.salon_name) 
            settings.address = request.POST.get("address", settings.address)
            settings.contact_number = request.POST.get("contact_number", settings.contact_number)
            settings.email = request.POST.get("email", settings.email)
            settings.opening_time = request.POST.get("opening_time") or settings.opening_time
            settings.closing_time = request.POST.get("closing_time") or settings.closing_time
        else:
            # create
            settings = SalonSettings.objects.create( # it creates a new SalonSettings object with the provided data from the POST request.
                salon_name=request.POST.get("salon_name"), # this line retrieves the value of "salon_name" from the POST request data. If the key is not present, it defaults to an empty string.
                address=request.POST.get("address", ""),
                contact_number=request.POST.get("contact_number", ""),
                email=request.POST.get("email", ""),
                opening_time=request.POST.get("opening_time") or None,# if opening_time is not provided, it sets it to None, i used None to show that the field can be empty in the database.
                closing_time=request.POST.get("closing_time") or None,
            )
        settings.save()
        return redirect("owner_dashboard")

    return render(request, "salon_settings.html", {"settings": settings})

@login_required
def owner_dashboard(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only salon admin can access this page.")

    today = timezone.now().date()

    total_staff = StaffProfile.objects.count()
    present_today = StaffAttendance.objects.filter(date=today, status="Present").count()
    absent_today = StaffAttendance.objects.filter(date=today, status="Absent").count()

    settings = SalonSettings.objects.first()
    context = {
        "today": today,
        "total_staff": total_staff,
        "present_today": present_today,
        "absent_today": absent_today,
        "settings": settings,
    }
    return render(request, "dashboard.html", context)

@login_required
def owner_staff_list(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only salon admin can access this page.")
    staff_profiles = StaffProfile.objects.select_related("user").all()
    return render(request, "owner_staff_list.html", {"staff_profiles": staff_profiles})


@login_required
def owner_staff_attendance(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only salon admin can access this page.")
    attendances = StaffAttendance.objects.select_related("staff", "staff__user").all()
    return render(request, "owner_staff_attendance.html", {"attendances": attendances})


@login_required
def owner_working_hours(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only salon admin can access this page.")
    from salon_app.models import WorkingHours
    working_hours = WorkingHours.objects.select_related("staff", "staff__user").all()
    return render(request, "owner_working_hours.html", {"working_hours": working_hours})

@login_required
def owner_profile_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only salon admin can access this page.")
    profile, created = owner_profile.objects.get_or_create(user=request.user)# here we are getting the owner profile for the logged in user, if it does not exist we create a new one.profile is storing the owner profile objects like phone number,address etc, , created ek boolean value hai jo batata hai ki naya object create hua hai ya nahi.

    if request.method == "POST":
        profile.phone_number = request.POST.get("phone_number", profile.phone_number)
        profile.address = request.POST.get("address", profile.address)
        profile.save()
        return redirect("owner_profile")

    context = {
        "profile": profile,
    }
    return render(request, "owner_profile.html", context)

@login_required
def staff_registration(request): # this view is for staff registration in which only admin can login the staff 
    if not request.user.is_superuser:
        return HttpResponseForbidden("Only admin can create staff accounts.")

    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            StaffProfile.objects.create(user=user)
            messages.success(request, 'Staff account has been created successfully.')
            return redirect('owner_dashboard')  # admin panel par wapas
    else:
        form = CustomRegistrationForm()
    return render(request, 'staff_registration.html', {'form': form})
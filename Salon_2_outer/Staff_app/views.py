from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from Staff_app.forms import StaffProfileForm
from Staff_app.models import StaffProfile
from customer_app.forms import CustomRegistrationForm

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import StaffProfile
from .serializers import StaffProfileSerializer

# ---------- PUBLIC STAFF LIST / DETAIL ----------

def staff_list_view(request):# It shows the list staff profile to the users who are visiting the website 
    staff_profiles = StaffProfile.objects.filter(user__is_staff=True)
    return render(request, "staff/staff_list.html", {"staff_profiles": staff_profiles})


@login_required
def staff_detail(request, pk):# this view is for showing staff details in the staff list 
    staff = get_object_or_404(StaffProfile, pk=pk)#   this line 
    return render(request, "staff/staff_detail.html", {"staff": staff})

# ---------- STAFF SELF PROFILE ----------

@login_required
def staff_profile(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff only.")
        return redirect("home")

    staff_profile = StaffProfile.objects.filter(user=request.user).first()
    if not staff_profile:
        staff_profile = StaffProfile.objects.create(user=request.user)

    context = {
        "staff_profile": staff_profile,
        "services": staff_profile.Service.all(),
    }
    return render(request, "staff/staff_profile.html", context)


@login_required
def staff_profile_edit(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Staff only.")
        return redirect("home")

    staff_profile = StaffProfile.objects.filter(user=request.user).first()
    if not staff_profile:
        staff_profile = StaffProfile.objects.create(user=request.user)

    if request.method == "POST":
        form = StaffProfileForm(
            request.POST,
            request.FILES,
            instance=staff_profile,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Staff profile updated successfully.")
            return redirect("staff_profile")
    else:
        form = StaffProfileForm(instance=staff_profile)

    return render(request, "staff/staff_profile_edit.html", {"form": form})

# ---------- STAFF REGISTRATION (by owner or admin) ----------

def staff_registration(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            StaffProfile.objects.create(user=user)
            messages.success(request, "Staff account has been created successfully.")
            return redirect("home")
    else:
        form = CustomRegistrationForm()
    return render(request, "staff_registration.html", {"form": form})

class StaffProfileViewSet(viewsets.ModelViewSet):
    queryset = StaffProfile.objects.all()# this line id used to get all the staff profile objects from the database.
    serializer_class = StaffProfileSerializer
    
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':# this line check karti hai ki agar user list ya retrieve action perform kar raha hai to usko allow any permission di jaye taki wo bina login kiye bhi staff profile dekh sake, lekin agar wo create, update ya delete action perform kar raha hai to usko is authenticated permission di jaye taki wo sirf apne profile ko hi edit kar sake.
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes] # this line gives the permission to the user based on the action they are trying to perform, permission() is used to create an instance of the permission class.
    
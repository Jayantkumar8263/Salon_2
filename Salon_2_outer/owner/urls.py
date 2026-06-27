from django.urls import path
from owner.views import owner_profile_view, salon_settings_view, owner_dashboard,owner_staff_list, owner_staff_attendance, owner_working_hours, staff_registration
# from salon_app.views import staff_registration

urlpatterns = [
    path('owner/dashboard/', owner_dashboard, name='owner_dashboard'),
    path('owner/settings/', salon_settings_view, name='salon_settings'),
    path('owner/profile/', owner_profile_view, name='owner_profile'),
    path('owner/staff/', owner_staff_list, name='owner_staff_list'),
    path('owner/staff/attendance/', owner_staff_attendance, name='owner_staff_attendance'),
    path('owner/staff/working-hours/', owner_working_hours, name='owner_working_hours'),
    path('staff_registration/', staff_registration, name='staff_registration'),
]

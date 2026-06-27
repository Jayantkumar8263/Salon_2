from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('staff/', views.staff_list_view, name='staff_profiles'),
    path('staff/<int:pk>/', views.staff_detail, name='staff_detail'),

    # Staff self profile
    path('staff/profile/', views.staff_profile, name='staff_profile'),
    path('staff/profile/edit/', views.staff_profile_edit, name='staff_profile_edit'),

    # Admin creates staff
    path('staff/register/', views.staff_registration, name='staff_registration'),
]

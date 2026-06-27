from django.urls import path
from . import views
from .views import  appointmentlist_View, create_appointment, signup_view ,registration, u_login, signin_view, u_logout, u_profile, appointmentform_view, appointmentdetail_view, appointment_edit, appointment_cancle, profile_edit
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # Authentication & account
    path('registration/', registration, name='registration'),  # User registration
    path('signin/', signin_view, name='signin'),               # Custom sign-in
    path('login/', u_login, name='login'),                     # (if still used)
    path('signup/', signup_view, name='signup'),               # Sign-up form
    path('logout/', u_logout, name='logout'),                  # Logout

    # User profile
    path('profile/', u_profile, name='profile'),# View profile
    path('profile/edit/', profile_edit, name='profile_edit'),  # Edit profile

    # Appointments
    path('appointments/', appointmentlist_View, name='appointment_list'),          # List appointments
    path('appointments/new/', create_appointment, name='create_appointment'),      # Create appointment
    path('appointment_form/', appointmentform_view, name='appointment_form'),      # Plain form page
    path('appointments/<int:pk>/', appointmentdetail_view, name='appointment_detail'),   # Detail
    path('appointments/<int:pk>/edit/', appointment_edit, name='appointment_edit'),      # Edit
    path('appointments/<int:pk>/cancel/', appointment_cancle, name='appointment_cancel'),# Cancel
    path('appointments/book/service/<int:service_id>/',views.appointment_book_service,name='appointment_book_service'), # Book appointment for specific service, when user clicks on the service.

    
]

if settings.DEBUG: # this is only for development, it will serve media files during development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # we are using += to append this pattern to the existing urlpatterns list, in simpe words it will add this pattern to the existing list of url patterns, settings.MEDIA_URL is the base url for media files it is usually /media/ and settings.MEDIA_ROOT is the actual file system path where media files are stored, document_root=settings.MEDIA_ROOT tells Django where to find the actual files on the filesystem.
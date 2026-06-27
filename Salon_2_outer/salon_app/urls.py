from django.urls import path
from . import views
from .views import service_list, home, workinghours_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
#from django.contrib.auth import views as auth_views 

#app_name = 'salon'

urlpatterns = [
    # Home & main pages
    path('', home, name='home'),                               # Home page
    path('services/', service_list, name='service_list'),      # Services page
]

if settings.DEBUG: # this is only for development, it will serve media files during development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # we are using += to append this pattern to the existing urlpatterns list, in simpe words it will add this pattern to the existing list of url patterns, settings.MEDIA_URL is the base url for media files it is usually /media/ and settings.MEDIA_ROOT is the actual file system path where media files are stored, document_root=settings.MEDIA_ROOT tells Django where to find the actual files on the filesystem.
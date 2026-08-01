"""
WSGI config for Salon_2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""
# wsgi is used for deploying the Django application to a web server. It serves as the entry point for WSGI-compatible web servers to serve your project, so it is a bridge between the web server and your Django application. It allows the web server to communicate with your Django application and handle incoming requests.

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Salon_2.settings')

application = get_wsgi_application()

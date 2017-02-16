"""
WSGI config for main project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
## https://bitbucket.org/schinckel/django-gevent-websocket/

import os

from django.core.wsgi import get_wsgi_application
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
channel_layer = channels.asgi.get_channel_layer()

"""
WSGI config for geekshop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os, sys
sys.path.insert(0, '/home/django/DjangoFrameworkOptimization/geekshop')
sys.path.insert(1, '/home/django/DjangoFrameworkOptimization/geekshop/.env/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'geekshop.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

appc = Celery('backend')
from django.conf import settings
appc.config_from_object('django.conf:settings')
appc.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
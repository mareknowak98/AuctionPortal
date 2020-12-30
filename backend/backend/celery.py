from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

### run celery:
### celery -A backend worker -l info
###

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

appc = Celery('backend')
# from django.conf import settings
appc.config_from_object('django.conf:settings', namespace='CELERY')
appc.autodiscover_tasks(lambda : settings.INSTALLED_APPS)
# appc.autodiscover_tasks()


@appc.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
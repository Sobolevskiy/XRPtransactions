import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'XRPtransactions.settings')
from django.conf import settings

app = Celery('XRPtransactions')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

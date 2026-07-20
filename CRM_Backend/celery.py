import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRM_Backend.settings")  # ← replace with your actual settings module

app = Celery("CRM_Backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
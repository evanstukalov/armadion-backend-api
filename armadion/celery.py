import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "armadion.settings")

app = Celery("armadion")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

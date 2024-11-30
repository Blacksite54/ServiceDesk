import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.main.settings")

app = Celery("api.main")
app.config_from_object("django.conf:settings")

app.autodiscover_tasks()

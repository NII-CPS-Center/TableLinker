import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
settings = os.getenv("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings)

app = Celery("tablelinker")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registere
app.autodiscover_tasks()

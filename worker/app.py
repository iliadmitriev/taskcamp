from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskcamp.settings')

app = Celery('tasks')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.config_from_object('worker.config')

print(app.conf.broker_url)

app.autodiscover_tasks()

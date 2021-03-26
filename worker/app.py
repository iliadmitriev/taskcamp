from celery import Celery

app = Celery('tasks')


app.config_from_object('worker.config')

app.autodiscover_tasks()

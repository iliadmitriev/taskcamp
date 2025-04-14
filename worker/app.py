"""
Worker application configuration module.
"""

from os import environ as env

from celery import Celery

from worker import config

env.setdefault("DJANGO_SETTINGS_MODULE", "taskcamp.settings")

RABBIT_USER = env.get("RABBITMQ_DEFAULT_USER")
RABBIT_PASS = env.get("RABBITMQ_DEFAULT_PASS")
RABBIT_VHOST = env.get("RABBITMQ_DEFAULT_VHOST")
RABBIT_HOST = env.get("RABBITMQ_HOST")
RABBIT_PORT = env.get("RABBITMQ_PORT")

REDIS_RESULTS_BACKEND = env.get("REDIS_RESULTS_BACKEND", None)

if RABBIT_HOST and RABBIT_PORT and RABBIT_VHOST and RABBIT_USER and RABBIT_PASS:
    broker_url = f"pyamqp://{RABBIT_USER}:{RABBIT_PASS}@{RABBIT_HOST}:{RABBIT_PORT}/{RABBIT_VHOST}"
else:
    broker_url = None


celery_app = Celery("worker")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.conf.broker_url = broker_url

celery_app.conf.result_backend = REDIS_RESULTS_BACKEND

celery_app.config_from_object(config)

celery_app.autodiscover_tasks(["worker.email"])

queue_names_list = [x.name for x in config.task_queue]

celery_app.select_queues(queue_names_list)

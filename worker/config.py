from os import environ as env
from worker.app import app as celery_app

env.setdefault('DJANGO_SETTINGS_MODULE', 'taskcamp.settings')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')


RABBIT_USER = env.get('RABBITMQ_DEFAULT_USER')
RABBIT_PASS = env.get('RABBITMQ_DEFAULT_PASS')
RABBIT_VHOST = env.get('RABBITMQ_DEFAULT_VHOST')
RABBIT_HOST = env.get('RABBITMQ_HOST')
RABBIT_PORT = env.get('RABBITMQ_PORT')

if RABBIT_HOST and RABBIT_PORT \
        and RABBIT_VHOST and RABBIT_USER and RABBIT_PASS:
    broker_url = f'pyamqp://{RABBIT_USER}:{RABBIT_PASS}@' \
                    f'{RABBIT_HOST}:{RABBIT_PORT}/{RABBIT_VHOST}'


task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Moscow'
enable_utc = True

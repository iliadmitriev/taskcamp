"""
Celery workers configuration module.
"""

from kombu import Exchange, Queue

worker_prefetch_multiplier = 1

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Moscow"
enable_utc = True

task_routes = {"worker.email.*": {"queue": "email"}}

task_default_queue = "celery"
task_default_exchange = "celery"

task_default_exchange_type = "direct"

task_queue = {
    Queue("celery", Exchange("celery"), routing_key="celery"),
    Queue("email", Exchange("email"), routing_key="email"),
}

task_create_missing_queues = True

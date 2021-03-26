
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Moscow'
enable_utc = True

imports = ('worker.tasks.email',)

task_routes = {
        'worker.tasks.email.send_activation_email': {'queue': 'activation_email'}
    }

task_default_queue = 'default'

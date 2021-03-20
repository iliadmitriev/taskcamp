from django import template
from projects.models import TaskStatus
from django.utils import timezone


register = template.Library()


@register.filter(name='task_class', is_safe=True)
def task_class(task):
    if (task.status in [TaskStatus.NEW, TaskStatus.IN_PROGRESS]) \
            and (task.end <= timezone.now()):
        return 'table-warning'
    if task.status == TaskStatus.CLOSED:
        return 'table-success'
    return ''

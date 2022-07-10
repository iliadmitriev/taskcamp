from django import template
from django.utils import timezone

from projects.models import TaskStatus

register = template.Library()


@register.filter(name="task_class", is_safe=True)
def task_class(task):
    if task.status == TaskStatus.CLOSED:
        return "table-success"
    if task.end is None:
        return ""
    if (task.status in [TaskStatus.NEW, TaskStatus.IN_PROGRESS]) and (
        task.end <= timezone.now()
    ):
        return "table-warning"
    return ""

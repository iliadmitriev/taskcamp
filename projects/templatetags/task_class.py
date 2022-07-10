"""
Task class filters for Jinja2 template.

Methods:
    task_class: Register filter for generating html-tag classname.

Attributes:
    register (Library): template library.
"""

from django import template
from django.utils import timezone

from projects.models import TaskStatus, Task

register = template.Library()


@register.filter(name="task_class", is_safe=True)
def task_class(task: Task) -> str:
    """Register filter for generating html-tag classname.

    Generate classname depending on `Task` status.

    exceeded due date => 'able-warning'
    closed => "table-success"
    * => ''

    Args:
        task (Task):

    Returns:
        (str): classname
    """
    if task.status == TaskStatus.CLOSED:
        return "table-success"
    if task.end is None:
        return ""
    if (task.status in [TaskStatus.NEW, TaskStatus.IN_PROGRESS]) and (
        task.end <= timezone.now()
    ):
        return "table-warning"
    return ""

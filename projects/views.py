from django.views.generic import ListView
from django.db.models import Q, F, Count, FloatField, Case, When
from .models import Project, Task, TaskStatus


class ProjectsListView(ListView):
    template_name = 'project_list.html'
    queryset = Project.objects \
        .annotate(
            status_count=Count('task'),
            status_new=Count(
                'task',
                filter=Q(task__status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS])
            )
        )\
        .annotate(
            completed=Case(
                When(status_count=0, then=0.0),
                default=(100.0 * F('status_new') / F('status_count')),
                output_field=FloatField()
            )
        )


class TaskListView(ListView):
    template_name = 'task_list.html'
    model = Task

from django.views.generic import ListView
from .models import Project, Task


class ProjectsListView(ListView):
    template_name = 'projects_list.html'
    model = Project


class TaskListView(ListView):
    template_name = 'task_list.html'
    model = Task

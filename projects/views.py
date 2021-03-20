from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView
)
from django.db.models import Q, F, Count, FloatField, Case, When
from django.urls import reverse_lazy
from .models import Project, Task, TaskStatus
from .forms import ProjectModelForm


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


class ProjectDetailView(DetailView):
    template_name = 'project_detail.html'
    model = Project


class ProjectCreateView(CreateView):
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm
    success_url = reverse_lazy('project-list')


class ProjectEditView(UpdateView):
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm
    success_url = reverse_lazy('project-list')


class ProjectDeleteView(DeleteView):
    template_name = 'project_confirm_delete.html'
    model = Project
    success_url = reverse_lazy('project-list')


class TaskListView(ListView):
    template_name = 'task_list.html'
    model = Task

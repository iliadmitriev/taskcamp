from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView
)
from django.db.models import Q, F, Count, FloatField, Case, When
from django.urls import reverse_lazy
from .models import Project, Task, TaskStatus
from .forms import ProjectModelForm, TaskModelForm


class ProjectsListView(ListView):
    template_name = 'project_list.html'
    queryset = Project.objects \
        .annotate(
            status_count=Count('task'),
            status_new=Count(
                'task',
                filter=Q(task__status__in=[
                    TaskStatus.NEW,
                    TaskStatus.IN_PROGRESS
                ])
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = kwargs.get('object')
        tasks = Task.objects.filter(project=project).order_by('id')
        context['task_list'] = tasks

        completed_data = tasks.aggregate(
            total=Count('id'),
            done=Count('id', filter=Q(status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS]))
        )
        if completed_data.get('total'):
            context['completed'] = 100.0 * completed_data.get('done') / completed_data.get('total')
            context['total'] = completed_data.get('total')
        else:
            context['completed'] = 0
            context['total'] = 0

        return context


class ProjectCreateView(CreateView):
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.id})


class ProjectEditView(UpdateView):
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.id})


class ProjectDeleteView(DeleteView):
    template_name = 'project_confirm_delete.html'
    model = Project
    success_url = reverse_lazy('project-list')


class TaskListView(ListView):
    template_name = 'task_list.html'
    model = Task


class TaskDetailView(DetailView):
    template_name = 'task_detail.html'
    model = Task


class TaskCreateView(CreateView):
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm
    success_url = reverse_lazy('task-list')


class TaskUpdateView(UpdateView):
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm
    success_url = reverse_lazy('task-list')


class TaskDeleteView(DeleteView):
    template_name = 'task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('task-list')

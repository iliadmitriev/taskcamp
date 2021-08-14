from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q, F, Count, FloatField, Case, When
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy
from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView, View
)

from documents.views import DocumentUpload
from .forms import ProjectModelForm, TaskModelForm, CommentModelForm
from .models import Project, Task, TaskStatus, Comment


class ProjectsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'project_list.html'
    permission_required = 'projects.view_project'
    permission_denied_message = gettext_lazy('You have no permission to view Projects')
    queryset = Project.objects \
        .annotate(
        status_count=Count('task'),
        status_new=Count(
            'task',
            filter=~Q(task__status__in=[
                TaskStatus.NEW,
                TaskStatus.IN_PROGRESS
            ])
        )
    ) \
        .annotate(
        completed=Case(
            When(status_count=0, then=0.0),
            default=(100.0 * F('status_new') / F('status_count')),
            output_field=FloatField()
        )
    ) \
        .order_by('id')


class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.view_project']
    permission_denied_message = gettext_lazy('You have no permission to view Projects')
    template_name = 'project_detail.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project_id = self.kwargs.get('pk')
        tasks = Task.objects.filter(project_id=project_id) \
            .order_by('id') \
            .select_related('assignee')
        if self.request.user.has_perm('projects.view_task'):
            context['task_list'] = tasks

        completed_data = tasks.aggregate(
            total=Count('id'),
            completed=Case(
                When(total=0, then=0.0),
                default=
                100.0 * Cast(
                    Count('id', filter=~Q(status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS])),
                    output_field=FloatField()
                ) / Cast(
                    Count('id'), output_field=FloatField()
                ))
        )

        context['completed'] = completed_data.get('completed')
        context['total'] = completed_data.get('total')

        return context


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.add_project']
    permission_denied_message = gettext_lazy('You have no permission to create Projects')
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.id})


class ProjectEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.change_project']
    permission_denied_message = gettext_lazy('You have no permission to edit Projects')
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse_lazy('project-detail', kwargs={'pk': self.object.id})


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.delete_project']
    permission_denied_message = gettext_lazy('You have no permission to delete Projects')
    template_name = 'project_confirm_delete.html'
    model = Project
    ordering = 'id'
    success_url = reverse_lazy('project-list')


class TaskListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.view_task']
    permission_denied_message = gettext_lazy('You have no permission to view Tasks')
    template_name = 'task_list.html'
    model = Task
    ordering = 'id'
    paginate_by = 10

    def get_queryset(self):
        tasks = Task.objects.all().select_related('author', 'assignee')
        ordering = self.request.GET.get('order_by') or self.ordering
        if self.request.GET.get('q'):
            search = self.request.GET.get('q')
            tasks = tasks.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
            )

        return tasks.order_by(ordering)


class TaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.view_task']
    permission_denied_message = gettext_lazy('You have no permission to view Tasks')
    template_name = 'task_detail.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        comments = Comment.objects.filter(task=task).order_by('created')
        if self.request.user.has_perm('projects.view_comment'):
            context['comments'] = comments
        if self.request.user.has_perm('projects.add_comment'):
            context['comment_form'] = CommentModelForm
        return context


class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.add_task']
    permission_denied_message = gettext_lazy('You have no permission to view Tasks')
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy('projects-task-detail', kwargs={'pk': self.object.id})


class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.change_task']
    permission_denied_message = gettext_lazy('You have no permission to edit Tasks')
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy('projects-task-detail', kwargs={'pk': self.object.id})


class TaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.delete_task']
    permission_denied_message = gettext_lazy('You have no permission to delete Tasks')
    template_name = 'task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('projects-task-list')


class CommentCreate(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')
    permission_required = ['projects.add_comment']
    permission_denied_message = gettext_lazy('You have no permission to add Comment')

    def post(self, *args, **kwargs):
        task_id = kwargs.get('pk')
        try:
            task = Task.objects.get(pk=task_id)
            description = self.request.POST.get('description')
            comment = Comment.objects.create(task=task, description=description)
        except Task.DoesNotExist:
            return HttpResponseRedirect(reverse('projects-task-list'))

        return HttpResponseRedirect(reverse('projects-task-detail', kwargs=kwargs))


class TaskDocumentUpload(LoginRequiredMixin, DocumentUpload):
    login_url = reverse_lazy('accounts:login')
    model = Task
    model_field = 'documents'

    def get_success_url(self, *args, **kwargs):
        task_id = self.kwargs.get('pk')
        return reverse('projects-task-detail', args=(task_id,))


class ProjectDocumentUpload(LoginRequiredMixin, DocumentUpload):
    login_url = reverse_lazy('accounts:login')
    model = Project
    model_field = 'documents'

    def get_success_url(self):
        project_id = self.kwargs.get('pk')
        return reverse('project-detail', args=(project_id,))

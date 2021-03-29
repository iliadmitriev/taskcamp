from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F, Count, FloatField, Case, When
from django.db import IntegrityError
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import Project, Task, TaskStatus, Comment
from .forms import ProjectModelForm, TaskModelForm, CommentModelForm
from documents.views import DocumentUpload


class ProjectsListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'project_list.html'
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
        )\
        .annotate(
            completed=Case(
                When(status_count=0, then=0.0),
                default=(100.0 * F('status_new') / F('status_count')),
                output_field=FloatField()
            )
        )\
        .order_by('id')


class ProjectDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'project_detail.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project_id = self.kwargs.get('pk')
        tasks = Task.objects.filter(project_id=project_id).order_by('id').select_related('assignee')
        context['task_list'] = tasks

        completed_data = tasks.aggregate(
            total=Count('id'),
            done=Count('id', filter=~Q(status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS]))
        )
        if completed_data.get('total'):
            context['completed'] = 100.0 * completed_data.get('done') / completed_data.get('total')
            context['total'] = completed_data.get('total')
        else:
            context['completed'] = 0
            context['total'] = 0

        return context


class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        return reverse_lazy('project-detail', kwargs={'pk': self.object.id})


class ProjectEditView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'project_form.html'
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse_lazy('project-detail', kwargs={'pk': self.object.id})


class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'project_confirm_delete.html'
    model = Project
    ordering = 'id'
    success_url = reverse_lazy('project-list')


class TaskListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('accounts:login')
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


class TaskDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'task_detail.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        comments = Comment.objects.filter(task=task).order_by('created')
        context['comments'] = comments
        context['comment_form'] = CommentModelForm
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy('projects-task-detail', kwargs={'pk': self.object.id})


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy('projects-task-detail', kwargs={'pk': self.object.id})


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('projects-task-list')


class CommentCreate(LoginRequiredMixin, View):
    login_url = reverse_lazy('accounts:login')

    def post(self, *args, **kwargs):
        task_id = kwargs.get('pk')
        try:
            description = self.request.POST.get('description')
            comment = Comment(task_id=task_id, description=description)
            comment.save()
        except IntegrityError:
            pass

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



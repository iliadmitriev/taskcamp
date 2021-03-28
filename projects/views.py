from django.views.generic import (
    ListView, DetailView, DeleteView,
    CreateView, UpdateView, View
)
from django.db.models import Q, F, Count, FloatField, Case, When
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from .models import Project, Task, TaskStatus, Comment
from .forms import ProjectModelForm, TaskModelForm, CommentModelForm
from documents.views import DocumentUpload


class ProjectsListView(ListView):
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


class ProjectDetailView(DetailView):
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
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return reverse_lazy('project-detail', kwargs={'pk': self.object.id})


class ProjectDeleteView(DeleteView):
    template_name = 'project_confirm_delete.html'
    model = Project
    ordering = 'id'
    success_url = reverse_lazy('project-list')


class TaskListView(ListView):
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


class TaskDetailView(DetailView):
    template_name = 'task_detail.html'
    model = Task

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        comments = Comment.objects.filter(task=task).order_by('created')
        context['comments'] = comments
        context['comment_form'] = CommentModelForm
        return context


class TaskCreateView(CreateView):
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy('projects-task-detail', kwargs={'pk': self.object.id})


class TaskUpdateView(UpdateView):
    template_name = 'task_form.html'
    model = Task
    form_class = TaskModelForm

    def get_success_url(self):
        return reverse_lazy('projects-task-detail', kwargs={'pk': self.object.id})


class TaskDeleteView(DeleteView):
    template_name = 'task_confirm_delete.html'
    model = Task
    success_url = reverse_lazy('projects-task-list')


class CommentCreate(View):
    def post(self, *args, **kwargs):
        task_id = kwargs.get('pk')
        try:
            description = self.request.POST.get('description')
            comment = Comment(task_id=task_id, description=description)
            comment.save()
        except IntegrityError:
            pass

        return HttpResponseRedirect(reverse('projects-task-detail', kwargs=kwargs))


class TaskDocumentUpload(DocumentUpload):

    def get_success_url(self, *args, **kwargs):
        task_id = self.kwargs.get('pk')
        return reverse('projects-task-detail', args=(task_id,))
    
    def form_valid(self, form):

        response = super(TaskDocumentUpload, self).form_valid(form)

        try:
            task_id = self.kwargs.get('pk')
            task = Task.objects.get(pk=task_id)
            task.documents.add(form.instance)
        except IntegrityError:
            pass

        return response


class ProjectDocumentUpload(DocumentUpload):
    def get_success_url(self):
        project_id = self.kwargs.get('pk')
        return reverse('project-detail', args=(project_id,))

    def form_valid(self, form):

        response = super(ProjectDocumentUpload, self).form_valid(form)

        try:
            project_id = self.kwargs.get('pk')
            project = Project.objects.get(pk=project_id)
            project.documents.add(form.instance)

        except IntegrityError:
            pass

        return response

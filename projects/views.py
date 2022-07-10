"""
Projects views module.
"""
from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Case, Count, F, FloatField, Q, When, QuerySet
from django.db.models.functions import Cast
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from documents.views import DocumentUpload

from .forms import CommentModelForm, ProjectModelForm, TaskModelForm
from .models import Comment, Project, Task, TaskStatus


class ProjectsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Project list view.

    Checks if user is logged in and user permissions.
    Redirects user to login page. Apply filters.
    Renders template.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        queryset (QuerySet): queryset for getting projects list.
    """

    login_url = reverse_lazy("accounts:login")
    template_name = "project_list.html"
    permission_required = "projects.view_project"
    permission_denied_message = gettext_lazy("You have no permission to view Projects")
    queryset = (
        Project.objects.annotate(
            status_count=Count("task"),
            status_new=Count(
                "task",
                filter=~Q(task__status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS]),
            ),
        )
        .annotate(
            completed=Case(
                When(status_count=0, then=0.0),
                default=(100.0 * F("status_new") / F("status_count")),
                output_field=FloatField(),
            )
        )
        .order_by("id")
    )


class ProjectDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Project detail view class.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model link to Project

    Methods:
        get_context_data: returns data for detail view rendering
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.view_project"]
    permission_denied_message = gettext_lazy("You have no permission to view Projects")
    template_name = "project_detail.html"
    model = Project

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Get from db all data for rendering detail view.

        Enriches project data with: list of tasks,
        completed tasks, total tasks, assignee

        Args:
            **kwargs: key value arguments with project id
        Returns:
            (dict) context data for rendering template
        """
        context = super().get_context_data(**kwargs)

        project_id = self.kwargs.get("pk")
        tasks = (
            Task.objects.filter(project_id=project_id)
            .order_by("id")
            .select_related("assignee")
        )
        if self.request.user.has_perm("projects.view_task"):
            context["task_list"] = tasks

        completed_data = tasks.aggregate(
            total=Count("id"),
            completed=Case(
                When(total=0, then=0.0),
                default=100.0 * Cast(
                    Count(
                        "id",
                        filter=~Q(status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS]),
                    ),
                    output_field=FloatField(),
                ) / Cast(Count("id"), output_field=FloatField()),
            ),
        )

        context["completed"] = completed_data.get("completed")
        context["total"] = completed_data.get("total")

        return context


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create Project view.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render create form
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model to create, link to Project
        form_class: link to class form

    Methods:
        get_success_url: returns success url path for redirect
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.add_project"]
    permission_denied_message = gettext_lazy(
        "You have no permission to create Projects"
    )
    template_name = "project_form.html"
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self) -> str:
        """Return success url path for redirect.

        Redirects to project detail view by project id.

        Returns:
            (str): success url path
        """
        return reverse_lazy("project-detail", kwargs={"pk": self.object.id})


class ProjectEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Project update view.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render edit form
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model to edit, link to Project
        form_class: link to class form

    Methods:
        get_success_url: returns success url path for redirect after update
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.change_project"]
    permission_denied_message = gettext_lazy("You have no permission to edit Projects")
    template_name = "project_form.html"
    model = Project
    form_class = ProjectModelForm

    def get_success_url(self) -> str:
        """Return success url path for redirect.

        Redirects to project detail view by project id
        or if the `next` parameter is specified to url address
        specified in `next` get parameter

        Returns:
            (str): success url path
        """
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return reverse_lazy("project-detail", kwargs={"pk": self.object.id})


class ProjectDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Project confirm deletion view.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render edit form
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model to delete, link to Project
        success_url (str): success url path for redirect after delete operation
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.delete_project"]
    permission_denied_message = gettext_lazy(
        "You have no permission to delete Projects"
    )
    template_name = "project_confirm_delete.html"
    model = Project
    ordering = "id"
    success_url = reverse_lazy("project-list")


class TaskListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Task list view.

    Checks if user is logged in and user permissions.
    Redirects user to login page. Apply filters.
    Renders template.

    Attributes:
        login_url (str): path to redirect not logged-in users
        ordering (str): default ordering string
        paginate_by (int): number of items per page
        template_name (str): template filename to render
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions

    Methods:
        get_queryset: queryset for getting Tasks list
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.view_task"]
    permission_denied_message = gettext_lazy("You have no permission to view Tasks")
    template_name = "task_list.html"
    model = Task
    ordering = "id"
    paginate_by = 10

    def get_queryset(self) -> QuerySet:
        """Get queryset for getting Tasks list.

        Returns:
            (QuerySet): queryset for getting Tasks list
        """
        tasks = Task.objects.all().select_related("author", "assignee")
        ordering = self.request.GET.get("order_by") or self.ordering
        if self.request.GET.get("q"):
            search = self.request.GET.get("q")
            tasks = tasks.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        return tasks.order_by(ordering)


class TaskDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Project detail view class.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model link to Task

    Methods:
        get_context_data: returns data for detail view rendering
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.view_task"]
    permission_denied_message = gettext_lazy("You have no permission to view Tasks")
    template_name = "task_detail.html"
    model = Task

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        """Get from db all data for rendering detail view.

        Enriches Task data with: list of Comments
        and Comment Form

        Args:
            **kwargs: key value arguments with Task id
        Returns:
            (dict) context data for rendering template
        """
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        comments = Comment.objects.filter(task=task).order_by("created")
        if self.request.user.has_perm("projects.view_comment"):
            context["comments"] = comments
        if self.request.user.has_perm("projects.add_comment"):
            context["comment_form"] = CommentModelForm
        return context


class TaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Create Project view.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render create `Task` form
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model to create, link to `Task`
        form_class: link to class form

    Methods:
        get_success_url: returns success url path for redirect
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.add_task"]
    permission_denied_message = gettext_lazy("You have no permission to view Tasks")
    template_name = "task_form.html"
    model = Task
    form_class = TaskModelForm

    def get_success_url(self) -> str:
        """Return success url path for redirect.

        Redirects to task detail view by task id.

        Returns:
            (str): success url path
        """
        return reverse_lazy("projects-task-detail", kwargs={"pk": self.object.id})


class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Task update view.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render edit form
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model to edit, link to `Task`
        form_class: link to class form

    Methods:
        get_success_url: returns success url path for redirect after update
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.change_task"]
    permission_denied_message = gettext_lazy("You have no permission to edit Tasks")
    template_name = "task_form.html"
    model = Task
    form_class = TaskModelForm

    def get_success_url(self) -> str:
        """Return success url path for redirect.

        Redirects to task detail view by task id.

        Returns:
            (str): success url path
        """
        return reverse_lazy("projects-task-detail", kwargs={"pk": self.object.id})


class TaskDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Task confirm deletion view.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        template_name (str): template filename to render edit form
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions
        model: model to delete, link to `Task`
        success_url (str): success url path for redirect after delete operation
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.delete_task"]
    permission_denied_message = gettext_lazy("You have no permission to delete Tasks")
    template_name = "task_confirm_delete.html"
    model = Task
    success_url = reverse_lazy("projects-task-list")


class CommentCreate(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Comment add view.

    Attributes:
        login_url (str): path to redirect not logged-in users.
        permission_required (str): permission requirements code
        permission_denied_message (str): message for user without permissions

    Methods:
        post: process incoming request and generate `HttpResponse`
    """

    login_url = reverse_lazy("accounts:login")
    permission_required = ["projects.add_comment"]
    permission_denied_message = gettext_lazy("You have no permission to add Comment")

    def post(self, *args, **kwargs) -> HttpResponse:
        """Add Comment to post.

        Accepts comment as request arguments.
        Checks and validates comment.
        Saves comment to database.
        Build HttpResponse.

        Args:
            *args: Request data
            **kwargs: Request data key-value format

        Returns:
            (HttpResponse) Http response (200 OK) on success
        """
        task_id = kwargs.get("pk")
        try:
            task = Task.objects.get(pk=task_id)
            description = self.request.POST.get("description")
            Comment.objects.create(task=task, description=description)
        except Task.DoesNotExist:
            return HttpResponseRedirect(reverse("projects-task-list"))

        return HttpResponseRedirect(reverse("projects-task-detail", kwargs=kwargs))


class TaskDocumentUpload(LoginRequiredMixin, DocumentUpload):
    """Upload document to `Task` FormView class."""

    login_url = reverse_lazy("accounts:login")
    model = Task
    model_field = "documents"

    def get_success_url(self, *args, **kwargs) -> str:
        """Return success url path for redirect.

        Redirects to task detail view by task id

        Returns:
            (str): success url path
        """
        task_id = self.kwargs.get("pk")
        return reverse("projects-task-detail", args=(task_id,))


class ProjectDocumentUpload(LoginRequiredMixin, DocumentUpload):
    """Upload document to `Project` FormView class."""

    login_url = reverse_lazy("accounts:login")
    model = Project
    model_field = "documents"

    def get_success_url(self) -> str:
        """Return success url path for redirect.

        Redirects to project detail view by task id

        Returns:
            (str): success url path
        """
        project_id = self.kwargs.get("pk")
        return reverse("project-detail", args=(project_id,))

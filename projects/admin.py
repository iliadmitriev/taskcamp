"""
Project admin config module.
"""

from typing import Optional

from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.urls import reverse

from .models import Comment, Project, Task


class ProjectAdmin(admin.ModelAdmin):
    """Project admin model.

    Attributes:
        readonly_fields (list): list of readonly fields
        fields (list): fields shown in detail view
        list_display (list): fields displayed in list view
        search_fields (list): fields used for full text search queries
        list_filter (list): fields used for left panel with filters

    """

    readonly_fields = ["id"]
    fields = ["id", "title", "description", "due_date", "is_closed"]
    list_display = ["id", "title", "description", "due_date", "is_closed"]
    search_fields = ["title", "description"]
    list_filter = ["due_date", "is_closed"]

    def get_view_on_site_url(self, obj: Optional[Project] = None) -> Optional[str]:
        """Get url path for link to site.

        Args:
            obj (Project): Project instance

        Returns:
            (str): path to project with this id on the site
        """
        return reverse("project-detail", args=(obj.id,)) if obj else None


class CommentInline(admin.TabularInline):
    """Inline admin comment.

    For display in Task admin detail view page.

    Attributes:
        extra (int): extra lines for adding new comments
        readonly_fields (list): list of uneditable fields
        fields (list): list of fields displayed in inline comment
        raw_id_fields (list): list of fields which is displayed
                   as an ids instead objects string as strings
    """

    model = Comment
    extra = 0
    readonly_fields = ["id", "created"]
    fields = ["id", "created", "task", "description"]
    raw_id_fields = ["task"]


class TaskAdmin(admin.ModelAdmin):
    """Task model admin.

    Attributes:
        list_select_related (bool): try to query related models in a single query,
                    instead of performing multiple queries for every object
        readonly_fields (list): list of uneditable fields
        fields (list): list of fields displayed in detail view page
        list_display (list): fields displayed in list view page
        search_fields (list): fields used for full text search queries
        list_filter (list): fields used for left panel with filters
        raw_id_fields (list): list of fields which is displayed
                   as an ids instead objects string as strings

        inlines (list): list of inlines attached to task object
    """

    list_select_related = True
    readonly_fields = ["id"]
    fields = [
        "id",
        "project",
        "title",
        "description",
        "start",
        "end",
        "author",
        "assignee",
        "status",
    ]
    list_display = [
        "id",
        "title",
        "project",
        "description",
        "start",
        "end",
        "author",
        "assignee",
        "status",
    ]
    search_fields = ["title", "description"]
    list_filter = ["status"]
    raw_id_fields = ["project", "author", "assignee"]

    inlines = [CommentInline]

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        """Return QuerySet instance to make queries for list and detail admin views.

        Args:
            request (HttpRequest): http request, needed here to get filters,
                    limits, page, and ordering.
        Returns:
            QuerySet instance
        """
        return (
            super(TaskAdmin, self).get_queryset(request).select_related("author", "assignee").select_related("project")
        )

    def get_view_on_site_url(self, obj: Optional[Task] = None) -> Optional[str]:
        """Get site url link for Task object.

        Args:
            obj: Task object

        Returns:
            (str): path to task with specified id on the site
        """
        return reverse("projects-task-detail", args=(obj.id,)) if obj else None


class CommentAdmin(admin.ModelAdmin):
    """Comment admin list and detail view class.

    list_select_related (bool): try to query related models in a single query,
                instead of performing multiple queries for every object
    readonly_fields (list): list of uneditable fields
    fields (list): list of fields displayed in detail view page
    list_display (list): fields displayed in list view page
    search_fields (list): fields used for full text search queries
    list_filter (list): fields used for left panel with filters
    raw_id_fields (list): list of fields which is displayed
               as an ids instead objects string as strings
    """

    list_select_related = True
    readonly_fields = ["id", "created"]
    fields = ["id", "created", "task", "description"]
    raw_id_fields = ["task"]
    search_fields = ["description"]
    list_display = ["id", "task", "created", "description"]

    def get_view_on_site_url(self, obj: Optional[Comment] = None) -> Optional[str]:
        """Get site url link for Comment object.

        Args:
            obj: Comment object

        Returns:
            (str): path to comment with specified id on task detail view.
        """
        return reverse("projects-task-detail", args=(obj.task.id,)) if obj else None


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Comment, CommentAdmin)

"""
Models for project module.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _

from documents.models import Document
from employees.models import Employee


class Project(models.Model):
    """Project django model.

    Attributes:
        title: project title
        description: project description
        due_date: project due date
        is_closed: is this project closed
        documents (Document): many-to-many, attached documents

    """

    title = models.CharField(verbose_name=_("Title"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), max_length=20000, null=True, blank=True)
    due_date = models.DateField(verbose_name=_("Due date"), null=True, blank=True)
    is_closed = models.BooleanField(verbose_name=_("Is closed"), default=False)

    documents = models.ManyToManyField(Document, verbose_name=_("Documents"))

    def __str__(self) -> str:
        """Project string representation."""
        return f"{self.id}: {self.title} ({self.is_closed})"

    class Meta:
        """Project names config."""

        verbose_name = _("Project")
        verbose_name_plural = _("Projects")


class TaskStatus(models.TextChoices):
    """Task statuses choice class."""

    NEW = "new", _("New")
    IN_PROGRESS = "in progress", _("In Progress")
    DONE = "done", _("Done")
    CLOSED = "closed", _("Closed")


class Task(models.Model):
    """Task model.

    Attributes:
        title:
        description:
        project (Project):
        start:
        end:
        author (Employee):
        assignee (Employee):
        status (TaskStatus):
        documnents (Document):

    """

    title = models.CharField(verbose_name=_("Title"), max_length=200)
    description = models.TextField(verbose_name=_("Description"), max_length=20000, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name=_("Project"), on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name=_("Start date"), null=True, blank=True)
    end = models.DateTimeField(verbose_name=_("End date"), null=True, blank=True)
    author = models.ForeignKey(
        Employee,
        related_name="author",
        verbose_name=_("Author"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    assignee = models.ForeignKey(
        Employee,
        related_name="assignee",
        verbose_name=_("Assignee"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    status = models.CharField(
        verbose_name=_("Status"),
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.NEW,
    )
    documents = models.ManyToManyField(Document, verbose_name=_("Documents"))

    def __str__(self) -> str:
        """Task string representation."""
        return f"{self.id}: {self.title} ({self.status})"

    class Meta:
        """Task config."""

        verbose_name = _("Task")
        verbose_name_plural = _("Tasks")


class Comment(models.Model):
    """Comment model.

    Args:
        task (Task): task comment link
        created: date and time of creation
        description: comment text
    """

    task = models.ForeignKey(Task, verbose_name=_("Task"), on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name=_("Created"), auto_now=True, db_index=True)
    description = models.TextField(
        verbose_name=_("Description"),
        max_length=5000,
    )

    class Meta:
        """Comment config."""

        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

from django.db import models
from django.utils.translation import gettext_lazy as _
from employees.models import Employee


class Project(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    description = models.CharField(verbose_name=_('Description'), max_length=2000)
    due_date = models.DateField(verbose_name=_('Due date'), null=True)
    is_closed = models.BooleanField(verbose_name=_('Is closed'), default=False)

    def __str__(self):
        return f'{self.id}: {self.title} ({self.is_closed})'

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')


class TaskStatus(models.TextChoices):
    NEW = 'new', _('New')
    IN_PROGRESS = 'in progress', _('In Progress')
    DONE = 'done', _('Done')
    CLOSED = 'closed', _('Closed')


class Task(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=200)
    description = models.CharField(verbose_name=_('Description'), max_length=2000)
    project = models.ForeignKey(Project, verbose_name=_('Project'), on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name=_('Start date'), null=True)
    end = models.DateTimeField(verbose_name=_('End date'), null=True)
    author = models.ForeignKey(
        Employee, related_name='author', verbose_name=_('Author'),
        null=True, on_delete=models.SET_NULL
    )
    assignee = models.ForeignKey(
        Employee, related_name='assignee', verbose_name=_('Assignee'),
        null=True, on_delete=models.SET_NULL
    )
    status = models.CharField(
        verbose_name=_('Status'), max_length=20,
        choices=TaskStatus.choices, default=TaskStatus.NEW
    )

    def __str__(self):
        return f'{self.id}: {self.title} ({self.status})'

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from django.urls import reverse_lazy
from projects.models import Project, Task, TaskStatus
from employees.models import Employee


class HomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.values('id').aggregate(
            total=Count('id'),
            in_progress=Count('id', filter=Q(is_closed=False)),
            completed=Count('id', filter=Q(is_closed=True)),
            overdue=Count('id', filter=Q(is_closed=False, due_date__lte=timezone.now()))
        )
        context['projects'] = projects
        tasks = Task.objects.values('id').aggregate(
            total=Count('id'),
            in_progress=Count(
                'id', filter=Q(
                    status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS]
                )
            ),
            overdue=Count(
                'id', filter=Q(
                    status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS],
                    end__lte=timezone.now()
                )
            ),
            completed=Count(
                'id', filter=Q(
                    status__in=[TaskStatus.DONE, TaskStatus.CLOSED]
                )
            )
        )
        context['tasks'] = tasks
        employees = Employee.objects \
            .values('id') \
            .annotate(
                assigned_count=Count('assignee'),
                assigned_today_count=Count(
                    'assignee',
                    filter=Q(
                        assignee__start__lte=timezone.now(),
                        assignee__end__gte=timezone.now(),
                        assignee__status__in=[TaskStatus.NEW, TaskStatus.IN_PROGRESS]
                    )
                )
            ) \
            .aggregate(
                total=Count('id'),
                assigned_for_today=Count('id', filter=Q(assigned_today_count__gt=0)),
                not_assigned_for_today=Count('id', filter=Q(assigned_today_count=0))
            )
        context['employees'] = employees

        return context

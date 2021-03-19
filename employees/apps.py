from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class EmployeesConfig(AppConfig):
    name = 'employees'
    verbose_name = _('Employees')


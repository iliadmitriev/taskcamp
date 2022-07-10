"""Employee application config."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EmployeesConfig(AppConfig):
    """Employee application config class."""

    name = "employees"
    verbose_name = _("Employees")

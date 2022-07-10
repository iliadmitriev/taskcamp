"""
Projects application config.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    """Projects application config class."""

    name = "projects"
    verbose_name = _("Projects")

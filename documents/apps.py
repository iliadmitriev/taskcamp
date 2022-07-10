"""
Documents application config.
"""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DocumentConfig(AppConfig):
    """Documents application config class."""

    name = "documents"
    verbose_name = _("Documents")

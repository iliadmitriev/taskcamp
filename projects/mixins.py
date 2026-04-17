"""
Projects view mixins module.

Provides reusable mixins for project and task views to reduce code duplication.
"""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class ProjectAuthMixin:
    """Mixin for project views with common authentication settings."""

    login_url = reverse_lazy("accounts:login")
    permission_denied_message = _("You don't have permission to perform this action.")


class TaskAuthMixin:
    """Mixin for task views with common authentication settings."""

    login_url = reverse_lazy("accounts:login")
    permission_denied_message = _("You don't have permission to perform this action.")


class ProjectURLMixin:
    """Mixin for project views with common URL patterns."""

    def get_success_url(self) -> str:
        """Return success URL for project operations."""
        return reverse_lazy("project-detail", kwargs={"pk": self.object.pk})

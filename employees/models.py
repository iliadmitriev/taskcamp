"""Employee models."""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):
    """Employee django model."""

    firstname = models.CharField(verbose_name=_("Firstname"), max_length=50)
    surname = models.CharField(verbose_name=_("Surname"), max_length=50)
    email = models.EmailField(verbose_name=_("Email"), max_length=100)
    birthdate = models.DateField(verbose_name=_("Birthdate"))

    def __str__(self) -> str:
        """Represent employee as string."""
        return f"{self.id}: {self.firstname} {self.surname}"

    def full_name(self) -> str:
        """Get employee full name."""
        return f"{self.firstname} {self.surname}"

    full_name.short_description = _("Full name")

    class Meta:
        """Employee model config."""

        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")

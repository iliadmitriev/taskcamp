"""Employee admin config module."""
from typing import Optional

from django.contrib import admin
from django.urls import reverse

from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    """Employee admin model."""

    list_display = ["id", "email", "firstname", "surname", "birthdate"]
    readonly_fields = ["id"]
    fields = ["id", "email", "firstname", "surname", "birthdate"]
    search_fields = ["email", "firstname", "surname"]

    def get_view_on_site_url(self, obj: Optional[Employee] = None) -> str:
        """Get url link to site for employee object."""
        return reverse("employee-detail", args=(obj.id,)) if obj else None


admin.site.register(Employee, EmployeeAdmin)

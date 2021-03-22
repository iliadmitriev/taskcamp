from django.contrib import admin
from django.urls import reverse
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'firstname', 'surname', 'birthdate']
    readonly_fields = ['id']
    fields = ['id', 'email', 'firstname', 'surname', 'birthdate']
    search_fields = ['email', 'firstname', 'surname']

    def get_view_on_site_url(self, obj=None):
        return reverse('employee-detail', args=(obj.id,))


admin.site.register(Employee, EmployeeAdmin)

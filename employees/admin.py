from django.contrib import admin
from .models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'firstname', 'surname', 'birthdate']
    readonly_fields = ['id']
    fields = ['id', 'email', 'firstname', 'surname', 'birthdate']
    search_fields = ['email', 'firstname', 'surname']


admin.site.register(Employee, EmployeeAdmin)

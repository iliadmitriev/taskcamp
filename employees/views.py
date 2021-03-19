from django.views.generic import ListView
from .models import Employee


class EmployeeListView(ListView):
    template_name = 'employee_list.html'
    model = Employee

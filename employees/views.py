from django.views.generic import ListView, DetailView
from .models import Employee


class EmployeeListView(ListView):
    template_name = 'employee_list.html'
    model = Employee


class EmployeeDetailView(DetailView):
    template_name = 'employee_detail.html'
    model = Employee

from django.views.generic import ListView, DetailView, DeleteView
from .models import Employee
from django.urls import reverse_lazy


class EmployeeListView(ListView):
    template_name = 'employee_list.html'
    model = Employee


class EmployeeDetailView(DetailView):
    template_name = 'employee_detail.html'
    model = Employee


class EmployeeDeleteView(DeleteView):
    template_name = 'employee_confirm_delete.html'
    model = Employee
    success_url = reverse_lazy('employee-list')

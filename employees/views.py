from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import EmployeeModelForm
from .models import Employee


class EmployeeListView(ListView):
    template_name = "employee_list.html"
    model = Employee
    ordering = "id"


class EmployeeDetailView(DetailView):
    template_name = "employee_detail.html"
    model = Employee


class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeModelForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee-list")


class EmployeeEditView(UpdateView):
    model = Employee
    form_class = EmployeeModelForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee-list")


class EmployeeDeleteView(DeleteView):
    template_name = "employee_confirm_delete.html"
    model = Employee
    success_url = reverse_lazy("employee-list")

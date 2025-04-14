"""Employee views module."""

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
    """Employee template list view."""

    template_name = "employee_list.html"
    model = Employee
    ordering = "id"


class EmployeeDetailView(DetailView):
    """Employee detail template view."""

    template_name = "employee_detail.html"
    model = Employee


class EmployeeCreateView(CreateView):
    """Employee create template form view."""

    model = Employee
    form_class = EmployeeModelForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee-list")


class EmployeeEditView(UpdateView):
    """Employee update template form view."""

    model = Employee
    form_class = EmployeeModelForm
    template_name = "employee_form.html"
    success_url = reverse_lazy("employee-list")


class EmployeeDeleteView(DeleteView):
    """Employee confirm delete template form view."""

    template_name = "employee_confirm_delete.html"
    model = Employee
    success_url = reverse_lazy("employee-list")

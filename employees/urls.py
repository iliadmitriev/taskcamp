from django.urls import path

from .views import (
    EmployeeCreateView,
    EmployeeDeleteView,
    EmployeeDetailView,
    EmployeeEditView,
    EmployeeListView,
)

urlpatterns = [
    path("", EmployeeListView.as_view(), name="employee-list"),
    path("add/", EmployeeCreateView.as_view(), name="employee-create"),
    path("<int:pk>/", EmployeeDetailView.as_view(), name="employee-detail"),
    path("<int:pk>/edit/", EmployeeEditView.as_view(), name="employee-edit"),
    path("<int:pk>/delete/", EmployeeDeleteView.as_view(), name="employee-delete"),
]

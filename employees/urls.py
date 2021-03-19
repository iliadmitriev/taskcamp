from django.urls import path
from .views import EmployeeListView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee-list')
]

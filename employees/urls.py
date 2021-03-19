from django.urls import path
from .views import EmployeeListView, EmployeeDetailView, EmployeeDeleteView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee-list'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete')
]

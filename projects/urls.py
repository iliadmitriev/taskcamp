from django.urls import path
from .views import (
    ProjectsListView, ProjectDetailView,
    ProjectCreateView, ProjectEditView,
    ProjectDeleteView,
    TaskListView
)


urlpatterns = [
    path('', ProjectsListView.as_view(), name='project-list'),
    path('add/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/edit/', ProjectEditView.as_view(), name='project-edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('tasks/', TaskListView.as_view(), name='projects-tasks-list')
]

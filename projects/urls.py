from django.urls import path
from .views import ProjectsListView, TaskListView


urlpatterns = [
    path('', ProjectsListView.as_view(), name='project-list'),
    path('add/', ProjectsListView.as_view(), name='project-create'),
    path('<int:pk>/', ProjectsListView.as_view(), name='project-detail'),
    path('<int:pk>/edit/', ProjectsListView.as_view(), name='project-edit'),
    path('<int:pk>/delete/', ProjectsListView.as_view(), name='project-delete'),
    path('tasks/', TaskListView.as_view(), name='projects-tasks-list')
]

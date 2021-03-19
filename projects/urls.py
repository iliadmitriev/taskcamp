from django.urls import path
from .views import ProjectsListView, TaskListView


urlpatterns = [
    path('', ProjectsListView.as_view(), name='projects-list'),
    path('tasks/', TaskListView.as_view(), name='projects-tasks-list')
]

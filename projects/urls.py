from django.urls import path
from .views import (
    ProjectsListView, ProjectDetailView,
    ProjectCreateView, ProjectEditView,
    ProjectDeleteView,
    TaskListView, TaskDetailView, TaskCreateView,
    TaskUpdateView, TaskDeleteView,
    CommentCreate
)


urlpatterns = [
    path('', ProjectsListView.as_view(), name='project-list'),
    path('add/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('<int:pk>/edit/', ProjectEditView.as_view(), name='project-edit'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('tasks/', TaskListView.as_view(), name='projects-task-list'),
    path('tasks/add/', TaskCreateView.as_view(), name='projects-task-create'),
    path('tasks/<int:pk>/', TaskDetailView.as_view(), name='projects-task-detail'),
    path('tasks/<int:pk>/comment/', CommentCreate.as_view(), name='comment-post'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='projects-task-edit'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='projects-task-delete'),
]

from django.urls import path
from .views import ProjectsIndexView


urlpatterns = [
    path('', ProjectsIndexView.as_view(), name='projects-list'),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home.urls')),
    path('projects/', include('projects.urls')),
    path('employees/', include('employees.urls')),
    path('admin/', admin.site.urls),
]

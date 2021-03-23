from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('home.urls')),
    path('projects/', include('projects.urls')),
    path('employees/', include('employees.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

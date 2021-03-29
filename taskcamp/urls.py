from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
import pkgutil


urlpatterns = [
    path('', include('home.urls')),
    path('projects/', include('projects.urls')),
    path('employees/', include('employees.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]


handler404 = 'taskcamp.views.http_404'
handler403 = 'taskcamp.views.http_403'
handler500 = 'taskcamp.views.http_500'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and pkgutil.find_loader('debug_toolbar'):
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

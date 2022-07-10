"""
Main urls router module for taskcamp.

All the routing starts here.

Attributes:
    urlpatterns: list of all paths
    handler404: name of method or a class for 404-page handler
    handler403: name of method or a class for 403-page handler
    handler500: name of method or a class for 500-page handler with exception

"""
import pkgutil

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import status_page

urlpatterns = [
    path("", include("home.urls")),
    path("projects/", include("projects.urls")),
    path("employees/", include("employees.urls")),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("status-page/", status_page),
]


handler404 = "taskcamp.views.http_404"
handler403 = "taskcamp.views.http_403"
handler500 = "taskcamp.views.http_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG and pkgutil.find_loader("debug_toolbar"):
    import debug_toolbar  # noqa

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

"""
Module for helper views.

Methods:
        http_404: 404-page handler
        http_403: 403-page handler
        http_500: 500-page handler
        status_page: status page handler function
"""

from django.db import OperationalError as dbOperationalError
from django.db import connections, router
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render
from psycopg2 import OperationalError as pgOperationalError


def http_404(request: HttpRequest, exception: Http404) -> HttpResponse:
    """Render and retrieve http response for 404 requests.

    Args:
        request: http request object
        exception: http 404 exception

    Returns:
        HttpResponse with status 404
    """
    data = {}
    return render(request, "handler/404.html", data, status=404)


def http_403(request: HttpRequest, exception: Exception) -> HttpResponse:
    """Render and retrieve http response for 403 requests.

    Args:
        request: http request object
        exception: exception

    Returns:
        HttpResponse with status 403
    """
    data = {"message": str(exception)}
    return render(request, "handler/403.html", data, status=403)


def http_500(request: HttpRequest) -> HttpResponse:
    """Render and retrieve 500 http response.

    Args:
        request: http request object

    Returns:
        HttpResponse with status 500
    """
    data = {}
    return render(request, "handler/500.html", data, status=500)


def status_page(request: HttpRequest) -> HttpResponse:
    """Check DB connection and retrieve status.

    Args:
        request: http GET request object

    Returns:
        HttpResponse with status 200 (ok) or 500 (error)
    """
    try:
        alias_for_write = router.db_for_write(model=None)
        db_conn = connections[alias_for_write]
        db_conn.connect()
    except (dbOperationalError, pgOperationalError):
        return HttpResponse("DB connection Fail", status=500)
    else:
        return HttpResponse("DB connection is OK", status=200)

from django.shortcuts import render
from django.http import HttpResponse
from django.db import router, connections
from psycopg2 import OperationalError as pgOperationalError
from django.db import OperationalError as dbOperationalError


def http_404(request, exception):
    data = {}
    return render(request, 'handler/404.html', data, status=404)


def http_403(request, exception):
    data = {'message': str(exception)}
    return render(request, 'handler/403.html', data, status=403)


def http_500(request):
    data = {}
    return render(request, 'handler/500.html', data, status=500)


def status_page(request):
    try:
        alias_for_write = router.db_for_write(model=None)
        db_conn = connections[alias_for_write]
        db_conn.connect()
    except (dbOperationalError, pgOperationalError):
        return HttpResponse("DB connection Fail", status=500)
    else:
        return HttpResponse("DB connection is OK", status=200)

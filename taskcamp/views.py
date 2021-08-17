from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection, OperationalError


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
        connection.ensure_connection()
    except OperationalError:
        return HttpResponse("DB connection Fail", status=500)
    else:
        return HttpResponse("DB connection is OK", status=200)

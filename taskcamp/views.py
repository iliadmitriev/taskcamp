from django.shortcuts import render


def http_404(request, exception):
    data = {}
    return render(request, 'handler/404.html', data, status=404)


def http_403(request, exception):
    data = {'message': str(exception)}
    return render(request, 'handler/403.html', data, status=403)


def http_500(request):
    data = {}
    return render(request, 'handler/500.html', data, status=500)

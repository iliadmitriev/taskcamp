from django.urls import path, include, reverse_lazy
from .views import AccountsLoginView

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('login/', AccountsLoginView.as_view(), name='login')
]
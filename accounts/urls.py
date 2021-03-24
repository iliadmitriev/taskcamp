from django.urls import path, include, reverse_lazy
from .views import AccountsLoginView, AccountsRegisterView

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register/', AccountsRegisterView.as_view(), name='register'),
    path('login/', AccountsLoginView.as_view(), name='login')
]
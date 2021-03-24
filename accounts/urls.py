from django.urls import path
from .views import (
    AccountsLoginView, AccountsRegisterView, AccountLogout
)

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register/', AccountsRegisterView.as_view(), name='register'),
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountLogout.as_view(), name='logout'),
]
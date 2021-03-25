from django.urls import path
from .views import (
    AccountsLoginView, AccountsRegisterView, AccountLogout,
    AccountsRegisterActivate, AccountsRegisterDoneView
)

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register/', AccountsRegisterView.as_view(), name='register'),
    path('register_done/', AccountsRegisterDoneView.as_view(), name='register-done'),
    path('activate/<str:user_hash>/<str:token>/', AccountsRegisterActivate.as_view(), name='activate'),
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountLogout.as_view(), name='logout'),
]
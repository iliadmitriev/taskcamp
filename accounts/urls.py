from django.urls import path
from .views import (
    AccountsLoginView, AccountsRegisterView, AccountLogout,
    AccountsRegisterActivate
)

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register/', AccountsRegisterView.as_view(), name='register'),
    path('activate/<str:user_hash>/<str:token>/', AccountsRegisterActivate.as_view(), name='activate'),
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountLogout.as_view(), name='logout'),
]
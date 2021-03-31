from django.urls import path
from .views import (
    AccountsLoginView, AccountsRegisterView, AccountsLogout,
    AccountsRegisterActivate, AccountsRegisterDoneView,
    AccountsPasswordResetView, AccountsPasswordResetDoneView,
    AccountsPasswordResetConfirm, AccountsPasswordResetComplete
)

app_name = 'accounts'

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('register/', AccountsRegisterView.as_view(), name='register'),
    path('register_done/', AccountsRegisterDoneView.as_view(), name='register-done'),
    path('activate/<str:user_hash>/<str:token>/', AccountsRegisterActivate.as_view(), name='activate'),
    path('login/', AccountsLoginView.as_view(), name='login'),
    path('logout/', AccountsLogout.as_view(), name='logout'),
    path('password_reset/', AccountsPasswordResetView.as_view(), name='password-reset'),
    path('password_reset_done/', AccountsPasswordResetDoneView.as_view(), name='password-reset-done'),
    path('password_reset_confirm/<str:uidb64>/<str:token>/',
         AccountsPasswordResetConfirm.as_view(), name='password-reset-confirm'),
    path('password_reset_complete/', AccountsPasswordResetComplete.as_view(),
         name='password-reset-complete')
]

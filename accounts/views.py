from django.contrib.auth import views as auth_views
from django.urls import reverse


class AccountsLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('home')


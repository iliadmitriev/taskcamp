from django.core.cache import cache
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.views.generic import FormView, View, TemplateView
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from .helpers import generate_user_hash_and_token
from worker.tasks.email import send_activation_email
from worker.app import app


class AccountsRegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('accounts:register-done')

    def form_valid(self, form):
        user_model = get_user_model()

        user = user_model.objects.create_user(
            form.cleaned_data.get('email'),
            form.cleaned_data.get('password1'),
            is_active=False
        )

        user_hash, token = generate_user_hash_and_token(user.id)

        url_link = '{}://{}{}'.format(
            self.request.scheme,
            get_current_site(self.request),
            reverse('accounts:activate', args=(user_hash, token,))
        )

        send_activation_email.delay(user.email, url_link)

        return super().form_valid(form)


class AccountsRegisterDoneView(TemplateView):
    template_name = 'register_done.html'

    def get_context_data(self, **kwargs):
        print(app.conf.task_routes)
        return {}


class AccountsRegisterActivate(View):

    def get(self, *args, **kwargs):
        user_hash = kwargs.get('user_hash')
        token = kwargs.get('token')
        user_model = get_user_model()

        data = cache.get(user_hash)

        if isinstance(data, dict) and data.get('token') == token:

            try:
                user_id = data.get('user_id')
                user = user_model.objects.get(pk=user_id)

                user.is_active = True
                user.save()

                login(self.request, user)

                cache.delete(user_hash)

                return HttpResponseRedirect(reverse('home'))

            except user_model.DoesNotExist:
                pass

        return HttpResponseBadRequest(b'hash is not found or expired')


class AccountsLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('home')


class AccountLogout(auth_views.LogoutView):
    next_page = reverse_lazy('accounts:login')

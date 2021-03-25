import uuid
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.views.generic import FormView, View, TemplateView
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import get_user_model
from .forms import RegisterForm


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

        user_hash, token = self.generate_user_hash_and_token(user.id)

        self.send_register_activation_email(user.email, user_hash, token)

        return super().form_valid(form)


    def generate_user_hash_and_token(self, user_id):
        user_hash = uuid.uuid4().hex
        token = uuid.uuid4().hex

        cache.set(
            user_hash,
            {
                'token': token,
                'user_id': user_id
            },
            settings.ACCOUNT_ACTIVATION_LINK_EXPIRE
        )
        return user_hash, token

    def send_register_activation_email(self, email, user_hash, token):
        url_link = '{}://{}{}'.format(
            self.request.scheme,
            get_current_site(self.request),
            reverse('accounts:activate', args=(user_hash, token,))
        )

        subject = 'Your account activation'

        html_message = render_to_string(
            'email/register_activate.html',
            {'url_link': url_link}
        )

        txt_message = render_to_string(
            'email/register_activate.txt',
            {'url_link': url_link}
        )

        message = EmailMultiAlternatives(
            subject,
            txt_message,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

        message.attach_alternative(html_message, 'text/html')

        return message.send()


class AccountsRegisterDoneView(TemplateView):
    template_name = 'register_done.html'


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

from typing import Optional

from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, AbstractUser
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView, View

from worker.email.tasks import send_activation_email, send_welcome_message

from .forms import AccountProfileForm, AccountsPasswordResetForm, RegisterForm
from .helpers import generate_user_hash_and_token


class AccountsRegisterView(FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("accounts:register-done")

    def form_valid(self, form: RegisterForm) -> HttpResponse:
        user_model = get_user_model()

        user = user_model.objects.create_user(
            form.cleaned_data.get("email"),
            form.cleaned_data.get("password1"),
            is_active=False,
        )

        try:
            group_public = Group.objects.get(name="public")
            user.groups.add(group_public)
        except Group.DoesNotExist:
            pass

        user_hash, token = generate_user_hash_and_token(user.id)

        url_link = "{}://{}{}".format(
            self.request.scheme,
            get_current_site(self.request),
            reverse(
                "accounts:activate",
                args=(
                    user_hash,
                    token,
                ),
            ),
        )

        send_activation_email.delay(user.email, url_link)

        return super().form_valid(form)


class AccountsRegisterDoneView(TemplateView):
    template_name = "register_done.html"


class AccountsRegisterActivate(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        user_hash = kwargs.get("user_hash")
        token = kwargs.get("token")
        user_model = get_user_model()

        data = cache.get(user_hash)

        if isinstance(data, dict) and data.get("token") == token:

            try:
                user_id = data.get("user_id")
                user = user_model.objects.get(pk=user_id)

                user.is_active = True
                user.save()

                login(self.request, user)

                cache.delete(user_hash)

                tour_link = "{}://{}{}".format(
                    self.request.scheme, get_current_site(self.request), reverse("home")
                )

                send_welcome_message.delay(user.email, tour_link)

                return HttpResponseRedirect(reverse("home"))

            except user_model.DoesNotExist:
                pass

        return HttpResponseBadRequest(b"hash is not found or expired")


class AccountsLoginView(auth_views.LoginView):
    template_name = "login.html"

    def get_success_url(self) -> str:
        url = self.get_redirect_url()
        return url or reverse("home")


class AccountsLogout(auth_views.LogoutView):
    next_page = reverse_lazy("accounts:login")


class AccountsPasswordResetView(auth_views.PasswordResetView):
    template_name = "password_reset.html"
    success_url = reverse_lazy("accounts:password-reset-done")
    form_class = AccountsPasswordResetForm
    email_template_name = "email/password_reset_email.html"
    html_email_template_name = "email/password_reset_email_html.html"
    subject_template_name = "email/password_reset_email_subj.txt"


class AccountsPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = "password_reset_done.html"
    success_url = reverse_lazy("accounts:password-reset-confirm")


class AccountsPasswordResetConfirm(auth_views.PasswordResetConfirmView):
    template_name = "password_reset_confirm.html"
    success_url = reverse_lazy("accounts:password-reset-complete")


class AccountsPasswordResetComplete(auth_views.PasswordResetCompleteView):
    template_name = "password_reset_complete.html"


class AccountsProfile(LoginRequiredMixin, UpdateView):
    template_name = "account_profile.html"
    form_class = AccountProfileForm

    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset: Optional[QuerySet] = None) -> AbstractUser:
        user_model = get_user_model()
        user_id = self.request.user.id
        return user_model.objects.get(pk=user_id)

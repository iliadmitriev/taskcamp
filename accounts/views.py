from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login
from django.views.generic import FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model


from .forms import RegisterForm


class AccountsRegisterView(FormView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):

        user_model = get_user_model()

        user_model.objects.create_user(
            form.cleaned_data.get('email'),
            form.cleaned_data.get('password1')
        )

        user = authenticate(
            self.request,
            username=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password1')
        )

        login(self.request, user)

        return super().form_valid(form)


class AccountsLoginView(auth_views.LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or reverse('home')


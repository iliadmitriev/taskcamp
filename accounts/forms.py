from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.contrib.auth import get_user_model
from worker.email.tasks import send_reset_email


class RegisterForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']


class AccountsPasswordResetForm(PasswordResetForm):

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        # have to delete user from context,
        # because user is not serializable
        context.pop('user', None)
        # send build and send email via celery
        send_reset_email.delay(
            subject_template_name, email_template_name, context,
            from_email, to_email, html_email_template_name=html_email_template_name
        )



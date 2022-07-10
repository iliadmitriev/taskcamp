"""
Accounts Forms module.

Forms:

    + RegisterForm - register user form with
        deleted username field, and email field used instead of username

    + AccountsPasswordResetForm - password reset form.

    + AccountProfileForm - profile edit form.

"""
from typing import Any, Optional, Dict

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm, UserCreationForm
from django.forms import ModelForm

from worker.email.tasks import send_reset_email


class RegisterForm(UserCreationForm):
    """Register user with email form."""

    class Meta:
        """Meta config."""

        model = get_user_model()
        fields = ["email", "password1", "password2"]


class AccountsPasswordResetForm(PasswordResetForm):
    """Reset password form.

    Methods:
        send_mail: sends reset password email

    """

    def send_mail(
        self,
        subject_template_name: str,
        email_template_name: str,
        context: Dict[str, Any],
        from_email: str,
        to_email: str,
        html_email_template_name: Optional[str] = None,
    ) -> None:
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        # have to delete user from context,
        # because user is not serializable
        context.pop("user", None)
        # send build and send email via celery
        send_reset_email.delay(
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=html_email_template_name,
        )


class AccountProfileForm(ModelForm):
    """Edit user profile form."""

    class Meta:
        """Meta config."""

        model = get_user_model()
        fields = ["first_name", "last_name", "birthdate"]

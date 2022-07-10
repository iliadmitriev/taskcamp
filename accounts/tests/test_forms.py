from unittest import mock

from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import Client, TestCase


class AccountsPasswordResetFormTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.send_reset_email = mock.Mock()
        self.user = get_user_model().objects.create(
            email="test@example.com", password="password", is_active=True
        )

    def test_account_password_reset_form_submit_success(self):
        with mock.patch(
            "worker.email.tasks.send_reset_email.delay", self.send_reset_email
        ):
            response = self.client.post(
                reverse("accounts:password-reset"), data={"email": self.user.email}
            )
            self.send_reset_email.assert_called_once()
            self.assertRedirects(
                response,
                reverse("accounts:password-reset-done"),
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True,
            )

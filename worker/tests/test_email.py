from django.core import mail
from django.test import TestCase

from worker import celery_app
from worker.email.tasks import (
    send_activation_email,
    send_reset_email,
    send_welcome_message,
)


class TestMyCeleryWorker(TestCase):
    def setUp(self):
        celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
        mail.outbox = []

    def test_send_activation_email(self):
        res = send_activation_email("test_email@exmaple.com", "https://example.com/")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Your taskcamp account activation")
        self.assertEqual(res, 1)

    def test_send_welcome_message(self):
        res = send_welcome_message("test_email@exmaple.com", "https://example.com/")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Taskcamp welcomes you")
        self.assertEqual(res, 1)

    def send_reset_email_success(self, html=True):
        send_reset_email(
            subject_template_name="email/password_reset_email_subj.txt",
            email_template_name="email/password_reset_email.html",
            context={
                "protocol": "https",
                "domain": "example.com",
                "uid": "uidb64",
                "token": "token",
                "user": {"get_username": "name"},
            },
            from_email="from@example.com",
            to_email="to@example.com",
            html_email_template_name="email/password_reset_email_html.html"
            if html
            else None,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Reset password")

    def test_send_reset_email_html(self):
        self.send_reset_email_success(html=True)

    def test_send_reset_email_not_html(self):
        self.send_reset_email_success(html=False)

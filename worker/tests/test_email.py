from django.core import mail
from django.test import TestCase

from worker import celery_app
from worker.email.tasks import send_activation_email, send_welcome_message


class TestMyCeleryWorker(TestCase):
    def setUp(self):
        celery_app.conf.update(CELERY_ALWAYS_EAGER=True)
        mail.outbox = []

    def test_send_activation_email(self):
        res = send_activation_email('test_email@exmaple.com', 'https://example.com/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Your taskcamp account activation')
        self.assertEqual(res, 1)

    def test_send_welcome_message(self):
        res = send_welcome_message('test_email@exmaple.com', 'https://example.com/')
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Taskcamp welcomes you')
        self.assertEqual(res, 1)

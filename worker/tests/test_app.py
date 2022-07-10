import importlib
import os
from unittest import mock

from django.test import TestCase

from worker import app


class WorkerAppTestCase(TestCase):
    def setUp(self) -> None:
        os.environ.clear()

    def test_worker_app_init(self):
        with mock.patch.dict(
            "os.environ",
            {
                "RABBITMQ_HOST": "rabbitmq",
                "RABBITMQ_PORT": "5672",
                "RABBITMQ_DEFAULT_VHOST": "celery",
                "RABBITMQ_DEFAULT_USER": "celery",
                "RABBITMQ_DEFAULT_PASS": "password",
            },
        ):
            self.assertIsNotNone(os.environ.get("RABBITMQ_HOST"))
            importlib.reload(app)
            self.assertEqual(
                app.broker_url, "pyamqp://celery:password@rabbitmq:5672/celery"
            )

        self.assertIsNone(os.environ.get("RABBITMQ_HOST"))
        importlib.reload(app)
        self.assertIsNone(app.broker_url)

from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTest(TestCase):
    def setUp(self) -> None:
        self.user_model = get_user_model()

    def test_create_user_without_email_raise(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(
                email=None,
                password='password'
            )

    def test_create_superuser_without_attributes_raise(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(
                email='test@example.com',
                password='password',
                is_superuser=False
            )

        with self.assertRaises(ValueError):
            self.user_model.objects.create_superuser(
                email='test@example.com',
                password='password',
                is_staff=False
            )

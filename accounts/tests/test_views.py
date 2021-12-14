import uuid
from unittest import mock

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.cache import cache
from django.shortcuts import reverse
from django.test import Client, TestCase

from accounts.helpers import generate_user_hash_and_token


class AccountsRegisterViewTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru', enforce_csrf_checks=False)
        self.mock_send_activation_email = mock.Mock()

    def register_post(self, email):
        with mock.patch('worker.email.tasks.send_activation_email.delay',
                        self.mock_send_activation_email):
            response = self.client.post(
                reverse('accounts:register'),
                data={
                    'email': email,
                    'password1': 'password',
                    'password2': 'password'
                }
            )
            self.assertRedirects(
                response,
                reverse('accounts:register-done'),
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True
            )
            self.assertEqual(len(self.mock_send_activation_email.call_args), 2)
            self.assertEqual(self.mock_send_activation_email.call_count, 1)

    def test_account_register_get(self):
        response = self.client.post(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('register.html')

    def test_account_register_with_public_group_success(self):
        self.register_post('random_test_email@example.com')

    def test_account_register_without_public_group_success(self):
        Group.objects.get(name='public').delete()
        self.register_post('random_test_email@example.com')


class AccountsRegisterActivateViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')
        self.mock_send_welcome_message = mock.Mock()

    def test_register_activate_get_success(self):
        with mock.patch('worker.email.tasks.send_welcome_message.delay',
                        self.mock_send_welcome_message):
            user = get_user_model().objects.create_user(
                email='test_user@example.com',
                password='test_password',
                is_active=False
            )
            user_hash, token = generate_user_hash_and_token(user.id)
            self.assertIsNotNone(cache.get(user_hash))
            response = self.client.get(reverse('accounts:activate',
                                               kwargs={'user_hash': user_hash, 'token': token}))
            self.assertRedirects(
                response,
                reverse('home'),
                status_code=302,
                target_status_code=200,
                fetch_redirect_response=True
            )
            uid = self.client.session.get('_auth_user_id')
            logged_user = get_user_model().objects.get(pk=uid)
            self.assertEqual(logged_user, user)
            self.assertIsNone(cache.get(user_hash))
            self.assertEqual(self.mock_send_welcome_message.call_count, 1)

    def test_register_activate_user_does_not_exist(self):
        with mock.patch('worker.email.tasks.send_welcome_message.delay',
                        self.mock_send_welcome_message):
            user_hash, token = generate_user_hash_and_token(100)
            self.assertIsNotNone(cache.get(user_hash))
            response = self.client.get(reverse('accounts:activate',
                                               kwargs={'user_hash': user_hash, 'token': token}))
            self.assertEquals(response.status_code, 400)
            self.assertIsNotNone(cache.get(user_hash))
            self.assertEqual(self.mock_send_welcome_message.call_count, 0)

    def test_register_activate_hash_does_not_exists(self):
        with mock.patch('worker.email.tasks.send_welcome_message.delay',
                        self.mock_send_welcome_message):
            user_hash, token = uuid.uuid4().hex, uuid.uuid4().hex
            self.assertIsNone(cache.get(user_hash))
            response = self.client.get(reverse('accounts:activate',
                                               kwargs={'user_hash': user_hash, 'token': token}))
            self.assertEquals(response.status_code, 400)
            self.assertEqual(self.mock_send_welcome_message.call_count, 0)


class AccountsLoginViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru', enforce_csrf_checks=True)

    def test_login_success(self):
        user = get_user_model().objects.create_user(
            email='test_login_email@example.com',
            password='password',
            is_active=True
        )
        get = self.client.get(reverse('accounts:login'))
        self.assertEqual(get.status_code, 200)
        self.assertIn('csrf_token', get.context)
        self.assertIn('form', get.context)
        self.assertTemplateUsed('login.html')
        csrf_token = get.context['csrf_token']
        response = self.client.post(
            reverse('accounts:login'),
            data={
                'username': 'test_login_email@example.com',
                'password': 'password',
                'csrfmiddlewaretoken': csrf_token,
                'next': '/'
            },
            cookies=get.cookies,
            HTTP_REFERER=reverse('accounts:login')
        )
        self.assertRedirects(
            response,
            reverse('home'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        uid = self.client.session.get('_auth_user_id')
        logged_user = get_user_model().objects.get(pk=uid)
        self.assertEqual(logged_user, user)


class AccountsProfileTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')

    def test_get_profile_success(self):
        user = get_user_model().objects.create_user(
            email='test_login_email@example.com',
            password='password',
            is_active=True
        )
        self.client.force_login(user)
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('account_profile.html')
        self.assertIn('form', response.context)

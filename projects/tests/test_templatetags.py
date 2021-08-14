from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.shortcuts import reverse
from projects.views import TaskListView


class TaskListTestCase(TestCase):
    fixtures = ['data.json']

    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')
        # user with edit permissions
        self.user = get_user_model().objects.create_superuser(
            email='edit_user@example.com',
            password='password',
            is_active=True
        )
        self.client.login(
            email='edit_user@example.com',
            password='password',
        )

    def test_task_list_view_with_tags(self):
        response = self.client.get(reverse('projects-task-list'))
        self.assertEqual(response.status_code, 200)

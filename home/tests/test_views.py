from django.test import Client, TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model


class HomeViewStatsTestCase(TestCase):
    fixtures = ['test-stats.json']

    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')

        self.user = get_user_model().objects.create_superuser(
            email='edit_user@example.com',
            password='password',
            is_active=True
        )
        self.client.login(
            email='edit_user@example.com',
            password='password',
        )

    def test_home_stats_view_OK(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertIn('projects', response.context)
        self.assertIn('tasks', response.context)
        self.assertIn('employees', response.context)
        self.assertDictEqual(
            response.context['projects'],
            {'completed': 1, 'in_progress': 3, 'overdue': 3, 'total': 4}
        )
        self.assertDictEqual(
            response.context['tasks'],
            {'completed': 7, 'in_progress': 7, 'overdue': 7, 'total': 14}
        )
        self.assertDictEqual(
            response.context['employees'],
            {'assigned_for_today': 0, 'not_assigned_for_today': 6, 'total': 6}
        )

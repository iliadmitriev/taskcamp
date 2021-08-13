from django.test import TestCase, Client
from django.shortcuts import reverse


class ProjectListViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')

    def test_project_list_view_unauthorized_302(self):
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, 302)

from django.test import TestCase, Client
from django.shortcuts import reverse
from django.http import QueryDict


class ProjectListViewTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')

    def test_project_list_view_unauthorized_302(self):
        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, 302)
        q = QueryDict(mutable=True)
        q['next'] = reverse('project-list')
        self.assertRedirects(
            response,
            "{0}?{1}".format(reverse('accounts:login'), q.urlencode()),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

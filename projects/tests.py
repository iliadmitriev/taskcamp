from django.test import TestCase, Client
from django.shortcuts import reverse
from django.http import QueryDict
from django.contrib.auth import get_user_model
from projects.models import Project, Task, TaskStatus


class TestCaseWithUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='test_project@example.com',
            password='password',
            is_active=True
        )

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def view_unauthorized_302(self, source_page, **kwargs):
        response = self.client.get(reverse(source_page, **kwargs))
        self.assertEqual(response.status_code, 302)
        q = QueryDict(mutable=True)
        q['next'] = reverse(source_page, **kwargs)
        self.assertRedirects(
            response,
            "{0}?{1}".format(reverse('accounts:login'), q.urlencode()),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )


class ProjectListViewTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')

    def test_project_list_view_unauthorized_302(self):
        self.view_unauthorized_302(source_page='project-list')

    def test_project_list_view_authorized_empty(self):
        self.client.login(email='test_project@example.com', password='password')

        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['project_list'], [])
        self.client.logout()

    def test_project_list_view_authorized_not_empty(self):
        self.client.login(email='test_project@example.com', password='password')

        project1 = Project.objects.create(
            title='Test project 1',
            description='Test project 1',
            due_date='2020-01-01',
            is_closed=False
        )
        project1 = Project.objects.create(
            title='Test project 2',
            description='Test project 2',
            due_date='2020-02-01',
            is_closed=False
        )

        response = self.client.get(reverse('project-list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['project_list'],
            Project.objects.order_by('id'),
            transform=lambda x: x
        )
        self.client.logout()


class ProjectDetailViewTestCase(TestCaseWithUser):
    def test_project_detail_view_unauthorized_302(self):
        self.view_unauthorized_302(source_page='project-detail', kwargs={'pk': 1})

    def test_project_detail_view_authorized_empty_404(self):
        self.client.login(email='test_project@example.com', password='password')

        response = self.client.get(reverse('project-detail', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_project_detail_view_authorized_200_OK_empty_task_list(self):
        self.client.login(email='test_project@example.com', password='password')
        project1 = Project.objects.create(
            title='Test project 1',
            description='Test project 1',
            due_date='2020-01-01',
            is_closed=False
        )

        response = self.client.get(reverse('project-detail', kwargs={'pk': project1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='project_detail.html')
        self.assertQuerysetEqual(response.context['task_list'], [])
        self.assertEqual(response.context['total'], 0)
        self.assertEqual(response.context['completed'], 0)
        self.client.logout()

    def test_project_detail_view_authorized_200_OK_with_task_list(self):
        self.client.login(email='test_project@example.com', password='password')
        project1 = Project.objects.create(
            title='Test project 1',
            description='Test project 1',
            due_date='2020-01-01',
            is_closed=False
        )
        task1 = Task.objects.create(
            title='Task 1', description='Task 1',
            project=project1, status=TaskStatus.NEW
        )
        task2 = Task.objects.create(
            title='Task 2', description='Task 2',
            project=project1, status=TaskStatus.DONE
        )

        response = self.client.get(reverse('project-detail', kwargs={'pk': project1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='project_detail.html')
        self.assertQuerysetEqual(
            response.context['task_list'],
            Task.objects.filter(project=project1).order_by('id'),
            transform=lambda x: x
        )
        self.assertEqual(response.context['total'], 2)
        self.assertEqual(response.context['completed'], 50.0)
        self.client.logout()

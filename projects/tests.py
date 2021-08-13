from django.test import TestCase, Client
from django.shortcuts import reverse
from django.http import QueryDict
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from projects.models import Project, Task, TaskStatus


class TestCaseWithUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user without any permission
        user_with_no_permission = get_user_model().objects.create_user(
            email='test@example.com',
            password='password',
            is_active=True
        )
        cls.user_with_no_permission = user_with_no_permission
        # user with view permissions
        user = get_user_model().objects.create_user(
            email='test_project@example.com',
            password='password',
            is_active=True
        )
        try:
            group_public = Group.objects.get(name='public')
            user.groups.add(group_public)
        except Group.DoesNotExist:
            pass
        cls.user = user

        # user with edit permissions
        user_with_privileges = get_user_model().objects.create_user(
            email='test_user_edit@example.com',
            password='password',
            is_active=True
        )
        perms_add = Permission.objects \
            .exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'contenttypes']) \
            .filter(codename__startswith='add_')
        perms_edit = Permission.objects \
            .exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'contenttypes']) \
            .filter(codename__startswith='change_')
        perms_delete = Permission.objects \
            .exclude(content_type__app_label__in=['auth', 'admin', 'sessions', 'contenttypes']) \
            .filter(codename__startswith='delete_')

        user_with_privileges.groups.add(group_public)
        user_with_privileges.user_permissions.add(*perms_edit, *perms_add, *perms_delete)
        cls.user_with_privileges = user_with_privileges

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.user_with_privileges.delete()
        cls.user_with_no_permission.delete()

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

    def test_project_detail_view_authorized_200_OK_with_no_task_permission(self):
        user = get_user_model().objects.create_user(
            email='myuser1@example.com',
            password='password',
            is_active=True
        )

        self.client.logout()
        self.client.login(email='myuser1@example.com', password='password')
        perms = Permission.objects \
            .filter(codename__in=['view_project'])

        user.user_permissions.add(*perms)
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
        response = self.client.get(reverse('project-detail', kwargs={'pk': project1.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='project_detail.html')
        self.assertEqual(
            response.context.get('task_list'), None
        )


class ProjectCreateViewTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE='ru')
        self.client.login(email='test_project@example.com', password='password')

    def test_project_create_view_unauthorized_302(self):
        self.client.logout()
        self.view_unauthorized_302(source_page='project-create')

    def test_project_create_view_403_no_permissions(self):
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 403)

    def test_project_create_view_200_OK(self):
        self.client.logout()
        self.client.login(
            email='test_user_edit@example.com',
            password='password'
        )
        response = self.client.get(reverse('project-create'))
        self.assertEqual(response.status_code, 200)

    def test_project_create_view_post_success(self):
        self.client.logout()
        self.client.login(
            email='test_user_edit@example.com',
            password='password'
        )
        response = self.client.post(
            reverse('project-create'),
            data={
                'title': 'Created test project title',
                'description': 'Created test project description'
            }
        )
        self.assertRedirects(
            response,
            reverse('project-detail', kwargs={'pk': 1}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

    def test_project_edit_view_post_success_with_next(self):
        self.client.logout()
        self.client.login(
            email='test_user_edit@example.com',
            password='password'
        )
        q = QueryDict(mutable=True)
        q['next'] = reverse('project-list')
        project = Project.objects.create(
            title='Test project to be edited',
            description='Test project to be edited',
            due_date='2020-01-01',
            is_closed=False
        )

        response = self.client.post(
            "{}?{}".format(reverse('project-edit', kwargs={'pk': project.id}), q.urlencode()),
            data={
                'title': 'Edited test project',
                'description': 'Edited test project'
            }
        )
        self.assertRedirects(
            response,
            reverse('project-list'),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )
        response = self.client.post(
            reverse('project-edit', kwargs={'pk': project.id}),
            data={
                'title': 'Edited test project',
                'description': 'Edited test project'
            }
        )
        self.assertRedirects(
            response,
            reverse('project-detail', kwargs={'pk': project.id}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True
        )

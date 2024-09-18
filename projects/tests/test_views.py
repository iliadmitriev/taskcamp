from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import reverse
from django.test import Client, TestCase

from projects.models import Comment, Project, Task, TaskStatus


class TestCaseWithUser(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user without any permission
        user_with_no_permission = get_user_model().objects.create_user(
            email="test@example.com", password="password", is_active=True
        )
        cls.user_with_no_permission = user_with_no_permission
        # user with view permissions
        user = get_user_model().objects.create_user(
            email="test_project@example.com", password="password", is_active=True
        )
        group_public = Group.objects.get(name="public")
        user.groups.add(group_public)
        cls.user = user

        # user with edit permissions
        user_with_privileges = get_user_model().objects.create_user(
            email="test_user_edit@example.com", password="password", is_active=True
        )
        perms_add = Permission.objects.exclude(
            content_type__app_label__in=["auth", "admin", "sessions", "contenttypes"]
        ).filter(codename__startswith="add_")
        perms_edit = Permission.objects.exclude(
            content_type__app_label__in=["auth", "admin", "sessions", "contenttypes"]
        ).filter(codename__startswith="change_")
        perms_delete = Permission.objects.exclude(
            content_type__app_label__in=["auth", "admin", "sessions", "contenttypes"]
        ).filter(codename__startswith="delete_")

        user_with_privileges.groups.add(group_public)
        user_with_privileges.user_permissions.add(
            *perms_edit, *perms_add, *perms_delete
        )
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
        q["next"] = reverse(source_page, **kwargs)
        self.assertRedirects(
            response,
            "{0}?{1}".format(reverse("accounts:login"), q.urlencode()),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class ProjectListViewTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")

    def test_project_list_view_unauthorized_302(self):
        self.view_unauthorized_302(source_page="project-list")

    def test_project_list_view_authorized_empty(self):
        self.client.login(email="test_project@example.com", password="password")

        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["project_list"], [])
        self.client.logout()

    def test_project_list_view_authorized_not_empty(self):
        self.client.login(email="test_project@example.com", password="password")

        project1 = Project.objects.create(
            title="Test project 1",
            description="Test project 1",
            due_date="2020-01-01",
            is_closed=False,
        )
        project1 = Project.objects.create(
            title="Test project 2",
            description="Test project 2",
            due_date="2020-02-01",
            is_closed=False,
        )

        response = self.client.get(reverse("project-list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["project_list"],
            Project.objects.order_by("id"),
            transform=lambda x: x,
        )
        self.client.logout()


class ProjectDetailViewTestCase(TestCaseWithUser):
    def test_project_detail_view_unauthorized_302(self):
        self.view_unauthorized_302(source_page="project-detail", kwargs={"pk": 1})

    def test_project_detail_view_authorized_empty_404(self):
        self.client.login(email="test_project@example.com", password="password")

        response = self.client.get(reverse("project-detail", kwargs={"pk": 1000}))
        self.assertEqual(response.status_code, 404)
        self.client.logout()

    def test_project_detail_view_authorized_200_OK_empty_task_list(self):
        self.client.login(email="test_project@example.com", password="password")
        project1 = Project.objects.create(
            title="Test project 1",
            description="Test project 1",
            due_date="2020-01-01",
            is_closed=False,
        )

        response = self.client.get(
            reverse("project-detail", kwargs={"pk": project1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="project_detail.html")
        self.assertQuerySetEqual(response.context["task_list"], [])
        self.assertEqual(response.context["total"], 0)
        self.assertEqual(response.context["completed"], 0)
        self.client.logout()

    def test_project_detail_view_authorized_200_OK_with_task_list(self):
        self.client.login(email="test_project@example.com", password="password")
        project1 = Project.objects.create(
            title="Test project 1",
            description="Test project 1",
            due_date="2020-01-01",
            is_closed=False,
        )
        task1 = Task.objects.create(
            title="Task 1",
            description="Task 1",
            project=project1,
            status=TaskStatus.NEW,
        )
        task2 = Task.objects.create(
            title="Task 2",
            description="Task 2",
            project=project1,
            status=TaskStatus.DONE,
        )

        response = self.client.get(
            reverse("project-detail", kwargs={"pk": project1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="project_detail.html")
        self.assertQuerySetEqual(
            response.context["task_list"],
            Task.objects.filter(project=project1).order_by("id"),
            transform=lambda x: x,
        )
        self.assertEqual(response.context["total"], 2)
        self.assertEqual(response.context["completed"], 50.0)

    def test_project_detail_view_authorized_200_OK_with_no_task_permission(self):
        user = get_user_model().objects.create_user(
            email="myuser1@example.com", password="password", is_active=True
        )

        self.client.logout()
        self.client.login(email="myuser1@example.com", password="password")
        perms = Permission.objects.filter(codename__in=["view_project"])

        user.user_permissions.add(*perms)
        project1 = Project.objects.create(
            title="Test project 1",
            description="Test project 1",
            due_date="2020-01-01",
            is_closed=False,
        )
        task1 = Task.objects.create(
            title="Task 1",
            description="Task 1",
            project=project1,
            status=TaskStatus.NEW,
        )
        response = self.client.get(
            reverse("project-detail", kwargs={"pk": project1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="project_detail.html")
        self.assertEqual(response.context.get("task_list"), None)


class ProjectCreateViewTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.client.login(email="test_project@example.com", password="password")

    def test_project_create_view_unauthorized_302(self):
        self.client.logout()
        self.view_unauthorized_302(source_page="project-create")

    def test_project_create_view_403_no_permissions(self):
        response = self.client.get(reverse("project-create"))
        self.assertEqual(response.status_code, 403)

    def test_project_create_view_200_OK(self):
        self.client.logout()
        self.client.login(email="test_user_edit@example.com", password="password")
        response = self.client.get(reverse("project-create"))
        self.assertEqual(response.status_code, 200)

    def test_project_create_view_post_success(self):
        self.client.logout()
        self.client.login(email="test_user_edit@example.com", password="password")
        response = self.client.post(
            reverse("project-create"),
            data={
                "title": "Created test project title",
                "description": "Created test project description",
            },
        )
        import re

        result_id = re.search(r"/projects/(\d+)/", response.url)
        self.assertRedirects(
            response,
            reverse("project-detail", kwargs={"pk": result_id[1]}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_project_edit_view_post_success_with_next(self):
        self.client.logout()
        self.client.login(email="test_user_edit@example.com", password="password")
        q = QueryDict(mutable=True)
        q["next"] = reverse("project-list")
        project = Project.objects.create(
            title="Test project to be edited",
            description="Test project to be edited",
            due_date="2020-01-01",
            is_closed=False,
        )

        response = self.client.post(
            "{}?{}".format(
                reverse("project-edit", kwargs={"pk": project.id}), q.urlencode()
            ),
            data={"title": "Edited test project", "description": "Edited test project"},
        )
        self.assertRedirects(
            response,
            reverse("project-list"),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        response = self.client.post(
            reverse("project-edit", kwargs={"pk": project.id}),
            data={"title": "Edited test project", "description": "Edited test project"},
        )
        self.assertRedirects(
            response,
            reverse("project-detail", kwargs={"pk": project.id}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class TaskListViewTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.client.login(email="test_project@example.com", password="password")

    def test_task_list_view_unauthorized_302(self):
        self.client.logout()
        self.view_unauthorized_302(source_page="projects-task-list")

    def test_task_list_view_200_OK(self):
        project1 = Project.objects.create(
            title="Test project for tasks",
            description="Test project for tasks",
            due_date="2020-01-01",
            is_closed=False,
        )
        task1 = Task.objects.create(
            title="Task 1 #searchtag",
            description="Task 1",
            project=project1,
            status=TaskStatus.NEW,
        )
        task2 = Task.objects.create(
            title="Task 2",
            description="Task 2",
            project=project1,
            status=TaskStatus.DONE,
        )

        response = self.client.get(reverse("projects-task-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="task_list.html")
        self.assertQuerySetEqual(
            response.context["task_list"],
            Task.objects.all().order_by("id"),
            transform=lambda x: x,
        )

        q = QueryDict(mutable=True)
        q["order_by"] = "id"
        q["q"] = "#searchtag"
        response = self.client.get(
            "{}?{}".format(reverse("projects-task-list"), q.urlencode())
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["task_list"],
            Task.objects.all()
            .filter(
                Q(title__icontains="#searchtag")
                | Q(description__icontains="#searchtag")
            )
            .order_by("id"),
            transform=lambda x: x,
        )


class TaskListDetailTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.client.login(email="test_project@example.com", password="password")

    def test_task_detail_view_unauthorized_302(self):
        self.client.logout()
        self.view_unauthorized_302(source_page="projects-task-detail", kwargs={"pk": 1})

    def test_task_detail_view_404(self):
        response = self.client.get(reverse("projects-task-detail", kwargs={"pk": 1000}))
        self.assertEqual(response.status_code, 404)

    def test_task_detail_view_OK_empty_comment(self):
        task1 = Task.objects.create(
            title="Test task 1",
            description="Test task 1",
            project=Project.objects.create(title="Test project 1"),
        )
        comment = Comment.objects.create(
            description="test comment description", task=task1
        )

        response = self.client.get(
            reverse("projects-task-detail", kwargs={"pk": task1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="task_detail.html")
        self.assertQuerySetEqual(
            response.context["comments"],
            Comment.objects.filter(task=task1),
            transform=lambda x: x,
        )
        self.assertTrue("comments" in response.context)
        self.assertTrue("comment_form" in response.context)

    def test_task_detail_view_OK_no_comment_permission(self):
        self.client.logout()
        user = get_user_model().objects.create_user(
            email="myuser1@example.com", password="password", is_active=True
        )

        self.client.login(email="myuser1@example.com", password="password")
        perms = Permission.objects.filter(codename__in=["view_project", "view_task"])

        user.user_permissions.add(*perms)

        self.client.login(email="myuser1@example.com", password="password")
        task1 = Task.objects.create(
            title="Test task 1",
            description="Test task 1",
            project=Project.objects.create(title="Test project 1"),
        )

        response = self.client.get(
            reverse("projects-task-detail", kwargs={"pk": task1.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="task_detail.html")
        self.assertFalse("comments" in response.context)
        self.assertFalse("comment_form" in response.context)


class TaskCreateTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.client.login(email="test_project@example.com", password="password")

    def test_task_create_view_unauthorized_302(self):
        self.client.logout()
        self.view_unauthorized_302(source_page="projects-task-detail", kwargs={"pk": 1})

    def test_project_create_view_403_no_permissions(self):
        response = self.client.get(reverse("projects-task-create"))
        self.assertEqual(response.status_code, 403)

    def test_task_create_view_OK(self):
        self.client.logout()
        self.client.login(email="test_user_edit@example.com", password="password")
        project = Project.objects.create(title="Test project")
        response = self.client.post(
            reverse("projects-task-create"),
            data={
                "title": "Test task title",
                "project": project.id,
                "status": TaskStatus.NEW,
            },
        )

        import re

        result_id = re.search(r"/projects/tasks/(\d+)/", response.url)

        self.assertRedirects(
            response,
            reverse("projects-task-detail", kwargs={"pk": result_id[1]}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class TaskEditTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="en")
        self.client.login(email="test_user_edit@example.com", password="password")

    def test_task_update_view_success(self):
        task = Task.objects.create(
            title="Test task", project=Project.objects.create(title="Test project")
        )
        response = self.client.post(
            reverse("projects-task-edit", kwargs={"pk": task.id}),
            data={
                "title": "Test task title",
                "project": task.project.id,
                "status": TaskStatus.IN_PROGRESS,
            },
        )

        self.assertRedirects(
            response,
            reverse("projects-task-detail", kwargs={"pk": task.id}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class CommentCreateTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.client.login(email="test_project@example.com", password="password")

    def test_view_comments_in_task(self):
        task = Task.objects.create(
            title="Test task", project=Project.objects.create(title="Test project")
        )
        comment1 = Comment.objects.create(task=task, description="test comment 1")
        comment2 = Comment.objects.create(task=task, description="test comment 2")
        response = self.client.get(
            reverse("projects-task-detail", kwargs={"pk": task.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["comments"],
            Comment.objects.filter(task=task),
            transform=lambda x: x,
        )
        self.assertTrue("comments" in response.context)
        self.assertTrue("comment_form" in response.context)
        self.assertEqual(len(response.context["comments"]), 2)

    def test_comment_post_success(self):
        task = Task.objects.create(
            title="Test task", project=Project.objects.create(title="Test project")
        )
        response = self.client.post(
            reverse("comment-post", kwargs={"pk": task.id}),
            data={"description": "New comment"},
        )
        self.assertRedirects(
            response,
            reverse("projects-task-detail", kwargs={"pk": task.id}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )

    def test_comment_post_fail(self):
        response = self.client.post(
            reverse("comment-post", kwargs={"pk": 100}),
            data={"description": "New comment"},
        )

        self.assertRedirects(
            response,
            reverse("projects-task-list"),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )


class TaskDocumentUploadTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.client.login(email="test_user_edit@example.com", password="password")

    def test_task_document_upload(self):
        task = Task.objects.create(
            title="Test task", project=Project.objects.create(title="Test project")
        )
        text_file = SimpleUploadedFile(
            "file.txt", b"file content", content_type="text/plain"
        )
        response = self.client.post(
            reverse("task-document-upload", kwargs={"pk": task.id}),
            data={"document": text_file},
        )
        self.assertRedirects(
            response,
            reverse("projects-task-detail", kwargs={"pk": task.id}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertEqual(task.documents.count(), 1)
        self.assertEqual(task.documents.first().document.size, text_file.size)


class ProjectDocumentUploadTestCase(TestCaseWithUser):
    def setUp(self) -> None:
        self.client = Client(HTTP_ACCEPT_LANGUAGE="ru")
        self.client.login(email="test_user_edit@example.com", password="password")

    def test_task_document_upload(self):
        project = Project.objects.create(title="Test project")
        text_file = SimpleUploadedFile(
            "file.txt", b"project file content", content_type="text/plain"
        )
        response = self.client.post(
            reverse("project-document-upload", kwargs={"pk": project.id}),
            data={"document": text_file},
        )
        self.assertRedirects(
            response,
            reverse("project-detail", kwargs={"pk": project.id}),
            status_code=302,
            target_status_code=200,
            fetch_redirect_response=True,
        )
        self.assertEqual(project.documents.count(), 1)
        self.assertEqual(project.documents.first().document.size, text_file.size)

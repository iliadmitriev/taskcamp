from django.contrib.admin import AdminSite
from django.test import TestCase
from django.urls import reverse

from projects.admin import ProjectAdmin, TaskAdmin, CommentAdmin
from projects.models import Project, Task, Comment


class ProjectAdminTestCase(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(title='Test project')
        self.task1 = Task.objects.create(title='Task 1', project=self.project)
        self.task2 = Task.objects.create(title='Task 2', project=self.project)
        self.comment = Comment.objects.create(description='test comment', task=self.task1)
        self.project_admin = ProjectAdmin(model=Project, admin_site=AdminSite)
        self.task_admin = TaskAdmin(model=Task, admin_site=AdminSite)
        self.comment_admin = CommentAdmin(model=Comment, admin_site=AdminSite)

    def test_project_admin_view_on_site_url(self):
        url = self.project_admin.get_view_on_site_url(obj=self.project)
        self.assertEqual(url, reverse('project-detail', kwargs={'pk': self.project.id}))

    def test_task_admin_get_queryset(self):
        task_queryset = self.task_admin.get_queryset(request=None)
        self.assertEqual(task_queryset.all().count(), 2)
        self.assertTrue(task_queryset.query.select_related)

    def test_task_admin_view_on_site_url(self):
        url = self.task_admin.get_view_on_site_url(obj=self.task1)
        self.assertEqual(url, reverse('projects-task-detail', kwargs={'pk': self.task1.id}))

    def test_comment_admin_view_on_site_url(self):
        url = self.comment_admin.get_view_on_site_url(obj=self.comment)
        self.assertEqual(url, reverse('projects-task-detail', kwargs={'pk': self.comment.task.id}))


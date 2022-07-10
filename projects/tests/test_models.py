from django.test import TestCase

from projects.models import Project, Task


class ProjectsTestCase(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(title="Test project")
        self.task = Task.objects.create(title="Test task", project=self.project)

    def test_project_model_str(self):
        self.assertEqual(
            self.project.__str__(),
            f"{self.project.id}: {self.project.title} ({self.project.is_closed})",
        )

    def test_task_model_str(self):
        self.assertEqual(
            self.task.__str__(),
            f"{self.task.id}: {self.task.title} ({self.task.status})",
        )

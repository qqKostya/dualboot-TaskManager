from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from main.models import Task

CustomUser = get_user_model()


class TaskPermissionTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="user", password="testpassword"
        )

        self.staff_user = CustomUser.objects.create_user(
            username="staffuser", password="testpassword", is_staff=True
        )

        self.task = Task.objects.create(title="Test Task", author=self.user)

    def test_delete_task_staff(self):
        self.client.login(username="staffuser", password="testpassword")

        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_user(self):
        self.client.login(username="user", password="testpassword")

        response = self.client.delete(f"/api/tasks/{self.task.id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.assertTrue(Task.objects.filter(id=self.task.id).exists())

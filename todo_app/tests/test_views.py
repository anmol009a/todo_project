from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from todo_app.models import Todo


class TodoViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.todo = Todo.objects.create(
            title="Sample Task",
            description="Sample Description",
            status="OPEN",
        )

    def test_list_todos(self):
        response = self.client.get("/api/todos/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_create_todo(self):
        data = {
            "title": "New Task",
            "description": "New Description",
            "status": "OPEN",
        }
        response = self.client.post("/api/todos/", data)
        self.assertEqual(response.status_code, 201)

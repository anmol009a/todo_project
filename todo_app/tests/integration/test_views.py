from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from todo_app.models import Todo


class TodoIntegrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.todo_url = "/api/todos/"
        self.payload = {
            "title": "Test Todo",
            "description": "Integration test for creating a todo.",
            "status": "OPEN",
            "due_date": "2025-12-15",
            "tags": [{"name": "test"}, {"name": "integration"}],
        }
        self.todo = Todo.objects.create(
            title="Sample Task",
            description="Sample Description",
            status="OPEN",
        )

    def test_list_todos(self):
        response = self.client.get(self.todo_url)
        self.assertEqual(response.status_code, 200)
        todos = response.json()
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0]["title"], "Sample Task")

    def test_create_todo(self):
        response = self.client.post(self.todo_url, self.payload, format="json")
        self.assertEqual(response.status_code, 201)

        # Verify data in the database
        todo = Todo.objects.get(title="Test Todo")
        self.assertEqual(todo.description, self.payload["description"])
        self.assertEqual(todo.status, self.payload["status"])
        self.assertEqual(todo.due_date.isoformat(), self.payload["due_date"])

        # Verify tags
        tags = todo.tags.all()
        self.assertEqual(len(tags), 2)
        self.assertTrue(tags.filter(name="test").exists())
        self.assertTrue(tags.filter(name="integration").exists())

    def test_update_todo(self):
        data = {
            "title": "Updated Task",
            "description": "Updated Description",
            "status": "WORKING",
            "due_date": "2025-12-20",
            "tags": [{"name": "important"}],
        }

        self.client.put(f"{self.todo_url}{self.todo.id}/", data, format="json")

        # Verify updated data in the database
        updated_todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.title, data["title"])
        self.assertEqual(updated_todo.description, data["description"])
        self.assertEqual(updated_todo.status, data["status"])
        self.assertEqual(updated_todo.due_date.isoformat(), data["due_date"])

        # Verify updated tags
        tags = updated_todo.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertTrue(tags.filter(name="important").exists())

    def test_partial_update_todo(self):
        data = {"description": "Partially Updated Description"}
        response = self.client.patch(
            f"{self.todo_url}{self.todo.id}/", data, format="json"
        )
        self.assertEqual(response.status_code, 200)

        # Verify partially updated data in the database
        updated_todo = Todo.objects.get(id=self.todo.id)
        self.assertEqual(updated_todo.description, data["description"])
        self.assertEqual(updated_todo.title, "Sample Task")  # Unchanged field

    def test_delete_todo(self):
        response = self.client.delete(f"{self.todo_url}{self.todo.id}/")
        self.assertEqual(response.status_code, 204)

        # Verify the todo is deleted from the database
        with self.assertRaises(Todo.DoesNotExist):
            Todo.objects.get(id=self.todo.id)

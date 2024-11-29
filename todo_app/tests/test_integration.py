from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User

class TodoIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_full_todo_crud(self):
        # Create a todo
        create_data = {
            "title": "Integration Task",
            "description": "Integration Description",
            "status": "OPEN"
        }
        response = self.client.post("/api/todos/", create_data)
        self.assertEqual(response.status_code, 201)
        todo_id = response.json()["id"]

        # Read the created todo
        response = self.client.get(f"/api/todos/{todo_id}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Integration Task")

        # Update the todo
        update_data = {
            "title": "Updated Integration Task",
            "description": "Updated Description",
            "status": "WORKING"
        }
        response = self.client.put(f"/api/todos/{todo_id}/", update_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "Updated Integration Task")

        # Delete the todo
        response = self.client.delete(f"/api/todos/{todo_id}/")
        self.assertEqual(response.status_code, 204)

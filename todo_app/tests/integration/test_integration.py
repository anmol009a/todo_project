from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from todo_app.models import Todo, Tag


class TodoIntegrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.todo_url = "/api/todos/"

    def _create_todo(self, data):
        """Helper to create a todo via the API."""
        response = self.client.post(self.todo_url, data, format="json")
        self.assertEqual(
            response.status_code, 201, f"Failed to create todo: {response.content}"
        )
        return response.json()

    def _get_todo(self, todo_id):
        """Helper to get a todo via the API."""
        response = self.client.get(f"{self.todo_url}{todo_id}/")
        self.assertEqual(
            response.status_code,
            200,
            f"Failed to get todo with ID {todo_id}: {response.content}",
        )
        return response.json()

    def _update_todo(self, todo_id, data):
        """Helper to update a todo via the API."""
        response = self.client.put(f"{self.todo_url}{todo_id}/", data, format="json")
        self.assertEqual(
            response.status_code,
            200,
            f"Failed to update todo with ID {todo_id}: {response.content}",
        )
        return response.json()

    def _delete_todo(self, todo_id):
        """Helper to delete a todo via the API."""
        response = self.client.delete(f"{self.todo_url}{todo_id}/")
        self.assertEqual(
            response.status_code,
            204,
            f"Failed to delete todo with ID {todo_id}: {response.content}",
        )

    def test_full_todo_crud(self):
        # Step 1: Create a todo
        create_data = {
            "title": "Integration Task",
            "description": "Integration Description",
            "status": "OPEN",
            "tags": [{"name": "important"}],
        }
        todo = self._create_todo(create_data)

        # Verify the todo exists in the database
        self.assertTrue(
            Todo.objects.filter(id=todo["id"]).exists(),
            "Todo not found in database after creation.",
        )
        self.assertTrue(
            Tag.objects.filter(name="important").exists(),
            "Tag 'important' not found in database after creation.",
        )

        # Step 2: Read the created todo
        fetched_todo = self._get_todo(todo["id"])
        self.assertEqual(
            fetched_todo["title"], create_data["title"], "Fetched title does not match."
        )
        self.assertEqual(
            fetched_todo["tags"][0]["name"], "important", "Fetched tag does not match."
        )

        # Step 3: Update the todo
        update_data = {
            "title": "Updated Integration Task",
            "description": "Updated Description",
            "status": "WORKING",
            "tags": [{"name": "important"}, {"name": "urgent"}],
        }
        updated_todo = self._update_todo(todo["id"], update_data)

        # Verify the update in the database
        self.assertEqual(
            updated_todo["title"], update_data["title"], "Updated title does not match."
        )
        self.assertTrue(
            Tag.objects.filter(name="urgent").exists(),
            "Tag 'urgent' not found in database after update.",
        )
        self.assertEqual(
            Todo.objects.get(id=todo["id"]).tags.count(),
            2,
            "Incorrect number of tags after update.",
        )

        # Step 4: Delete the todo
        self._delete_todo(todo["id"])

        # Verify the todo and its tags are not associated anymore
        self.assertFalse(
            Todo.objects.filter(id=todo["id"]).exists(),
            "Todo not deleted from database.",
        )
        self.assertTrue(
            Tag.objects.filter(name="important").exists(),
            "Tag 'important' should not be deleted.",
        )

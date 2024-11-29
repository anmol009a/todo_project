from django.test import TestCase
from todo_app.models import Todo

class TodoModelTestCase(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Task",
            description="This is a test task.",
            status="OPEN"
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, "Test Task")
        self.assertEqual(self.todo.status, "OPEN")
        self.assertIsNotNone(self.todo.timestamp)

    def test_string_representation(self):
        self.assertEqual(str(self.todo), "Test Task")

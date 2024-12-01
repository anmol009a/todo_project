from django.test import TestCase
from todo_app.models import Todo
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import datetime, timedelta


class TodoModelTestCase(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Task",
            description="This is a test task.",
            status="OPEN",
            due_date="2024-12-01",
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, "Test Task")
        self.assertEqual(self.todo.status, "OPEN")
        self.assertIsNotNone(self.todo.timestamp)

    def test_string_representation(self):
        self.assertEqual(str(self.todo), "Test Task")

    def test_due_date_cannot_be_earlier_than_timestamp(self):
        # Case 1: Creating a Todo with a valid due date (after the timestamp)
        todo = Todo.objects.create(
            title="Test Todo 1",
            description="Description 1",
            due_date=now().date() + timedelta(days=1),  # Due date is tomorrow
        )
        try:
            todo.clean()  # Should not raise any validation error
        except ValidationError:
            self.fail("ValidationError raised unexpectedly!")

        # Case 2: Creating a Todo with a due date earlier than the timestamp
        todo_invalid = Todo.objects.create(
            title="Test Todo 2",
            description="Description 2",
            due_date=now().date() - timedelta(days=1),  # Due date is yesterday
        )
        with self.assertRaises(ValidationError):
            todo_invalid.clean()  # Should raise a validation error

    def test_due_date_is_optional(self):
        # Case 3: Creating a Todo with no due date (None)
        todo = Todo.objects.create(
            title="Test Todo 3",
            description="Description 3",
            due_date=None,  # No due date
        )
        try:
            todo.clean()  # Should not raise any validation error
        except ValidationError:
            self.fail("ValidationError raised unexpectedly for None due_date!")

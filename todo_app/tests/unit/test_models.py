from django.test import TestCase
from todo_app.models import Todo, Tag


class TodoModelTestCase(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(
            title="Test Task",
            description="This is a test task.",
            status="OPEN",
            due_date="2025-12-15",
        )

        # Create a tag and associate it with the todo
        tag, _ = Tag.objects.get_or_create(name="Test")
        self.todo.tags.add(tag)

    def test_todo_creation(self):
        # Test that the Todo was created correctly
        todo = Todo.objects.get(title="Test Task")
        self.assertEqual(todo.title, "Test Task")
        self.assertEqual(todo.description, "This is a test task.")
        self.assertEqual(todo.status, "OPEN")
        self.assertEqual(todo.due_date.isoformat(), "2025-12-15")
        self.assertIsNotNone(todo.timestamp)
        self.assertTrue(todo.tags.filter(name="Test").exists())

    def test_string_representation(self):
        # Test the string representation of the Todo
        self.assertEqual(str(self.todo), "Test Task")


class TagModelTestCase(TestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name="Test")
        return super().setUp()

    def test_tag_creation(self):
        tag = Tag.objects.get(name="Test")
        self.assertEqual(tag.name, "Test")

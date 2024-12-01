from django.test import TestCase
from todo_app.serializers import TodoSerializer


class TodoSerializerTestCase(TestCase):
    def test_todo_serializer(self):
        todo_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2024-12-01",
            "status": "OPEN",
        }
        serializer = TodoSerializer(data=todo_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "Test Task")

from django.test import TestCase
from todo_app.serializers import TodoSerializer


class TodoSerializerTestCase(TestCase):
    def test_todo_serializer(self):
        todo_data = {
            "title": "Test Task",
            "description": "Test Description",
            "due_date": "2050-12-30",
            "status": "OPEN",
            "tags": [{"name": "important"}],
        }
        serializer = TodoSerializer(data=todo_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "Test Task")

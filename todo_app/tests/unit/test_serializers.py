from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from todo_app.serializers import TodoSerializer


class TodoSerializerTest(TestCase):

    def setUp(self):
        # Set up some basic data to use for tests
        self.timestamp = timezone.now()
        self.todo_data_valid = {
            'title': 'Test Todo',
            'description': 'This is a test todo',
            'due_date': self.timestamp.date() + timedelta(days=1),
            'status': 'OPEN',
        }

    def test_todo_serializer_valid(self):
        # Test that the serializer correctly serializes valid data
        serializer = TodoSerializer(data=self.todo_data_valid)
        self.assertTrue(serializer.is_valid())
        todo = serializer.save()  # Save the valid data to the database
        self.assertEqual(todo.title, self.todo_data_valid['title'])
        self.assertEqual(todo.description, self.todo_data_valid['description'])
        self.assertEqual(todo.status, self.todo_data_valid['status'])

    def test_todo_serializer_invalid_due_date(self):
        # Test invalid due date (due date earlier than timestamp)
        invalid_data = self.todo_data_valid.copy()
        invalid_data['due_date'] = self.timestamp.date() - timedelta(
            days=1
        )  # Invalid: Due date is in the past
        serializer = TodoSerializer(data=invalid_data)

        # Check that the serializer is not valid due to the validation error
        self.assertFalse(serializer.is_valid())
        self.assertIn('due_date', serializer.errors)
        self.assertEqual(
            serializer.errors['due_date'][0],
            'Due date cannot be earlier than the creation timestamp.',
        )

    def test_todo_serializer_missing_due_date(self):
        # Test missing due date (optional field)
        valid_data_no_due_date = self.todo_data_valid.copy()
        valid_data_no_due_date.pop('due_date')
        serializer = TodoSerializer(data=valid_data_no_due_date)

        self.assertTrue(
            serializer.is_valid()
        )  # It should be valid even without due_date
        todo = serializer.save()
        self.assertIsNone(
            todo.due_date
        )  # Make sure the due_date is None when not provided

    def test_todo_serializer_status_validation(self):
        # Test invalid status value
        invalid_data = self.todo_data_valid.copy()
        invalid_data['status'] = 'INVALID_STATUS'  # Invalid status
        serializer = TodoSerializer(data=invalid_data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors)
        self.assertIn('not a valid choice.', serializer.errors['status'][0])

    def test_todo_serializer_with_tags(self):
        # Test Todo with tags (multiple tags)
        valid_data_with_tags = self.todo_data_valid.copy()
        valid_data_with_tags['tags'] = ['work', 'urgent', 'work']  # Duplicate 'work' tag
        serializer = TodoSerializer(data=valid_data_with_tags)

        self.assertTrue(serializer.is_valid())
        todo = serializer.save()
        self.assertEqual(
            len(todo.tags), 2
        )  # Only 'work' and 'urgent' tags should be saved, 'work' is deduplicated

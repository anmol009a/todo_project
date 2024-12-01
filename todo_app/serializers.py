from rest_framework import serializers
from .models import Todo
from django.utils.timezone import now


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('timestamp',)

    def validate_due_date(self, due_date):
        # Use current time as fallback if `timestamp` is not set
        timestamp = self.instance.timestamp if self.instance else now()

        if due_date and due_date < timestamp.date():
            raise serializers.ValidationError(
                "Due date cannot be earlier than the creation timestamp."
            )
        return due_date

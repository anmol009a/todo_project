from rest_framework import serializers
from todo_app.models import Todo, Tag
from django.utils.timezone import now


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]

        extra_kwargs = {
            'name': {'validators': []},  # remove default unique validation
        }


class TodoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = ('timestamp',)

    def create(self, validated_data):
        tags_data = validated_data.pop("tags", [])
        todo = Todo.objects.create(**validated_data)

        # Use set() to assign many-to-many relationships
        tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data["name"])
            tags.append(tag)
        todo.tags.set(tags)

        return todo

    def update(self, instance, validated_data):
        tags_data = validated_data.pop("tags", [])
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.status = validated_data.get("status", instance.status)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.save()

        # Update tags using set()
        tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_data["name"])
            tags.append(tag)
        instance.tags.set(tags)

        return instance

    def validate_due_date(self, due_date):
        # Use current time as fallback if `timestamp` is not set
        timestamp = self.instance.timestamp if self.instance else now()

        if due_date and due_date < timestamp.date():
            raise serializers.ValidationError(
                "Due date cannot be earlier than the creation timestamp."
            )
        return due_date

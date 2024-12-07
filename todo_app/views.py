from rest_framework import viewsets
from todo_app.models import Todo, Tag
from todo_app.serializers import TodoSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting todo items.
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer


class TodoViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, creating, updating, and deleting todo items.
    """

    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo_app.views import TodoViewSet, TagViewSet

router = DefaultRouter()
router.register(r"todos", TodoViewSet)
router.register(r"tags", TagViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

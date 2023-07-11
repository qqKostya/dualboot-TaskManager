from typing import cast
from rest_framework import viewsets
import django_filters
from task_manager.services.single_resource import (
    SingleResourceMixin,
    SingleResourceUpdateMixin,
)
from .models import User, Tag, Task
from .serializers import UserSerializer, TagSerializer, TaskSerializer
from .permissions import IsStaffOrReadOnly


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("name",)


class TaskViewSet(viewsets.ModelViewSet):
    state = django_filters.CharFilter(lookup_expr="icontains")
    tags = django_filters.MultipleChoiceFilter(lookup_expr="icontains")
    executor = django_filters.CharFilter(lookup_expr="icontains")
    author = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Tag
        fields = ("state", "tags", "executor", "author")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.prefetch_related("tags", "author", "executor").order_by(
        "id"
    )
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrReadOnly]


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)

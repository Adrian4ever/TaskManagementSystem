import django_filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, UserTasksSerializer, TaskSerializerNoOwner, TasksAssignedSerializer
from apps.users.get_user_model import USER_MODEL
from apps.users.serializers import UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskSerializerNoOwner
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, serializer_class=TasksAssignedSerializer)
    def my(self, request):
        tasks = Task.objects.filter(owner=self.request.user)
        return Response(TasksAssignedSerializer(tasks, many=True).data)


class UserListView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = USER_MODEL.objects.all()
        return Response(UserSerializer(users, many=True).data)

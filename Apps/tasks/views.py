import django_filters
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.db.models import Sum, F
from rest_framework import generics, filters
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskCreateSerializer, TasksInfoSerializer, TaskUpdateSerializer, \
    TaskUpdateStatusSerializer, TaskItemSerializer, TaskItemLogsSerializer
from apps.users.get_user_model import USER_MODEL
from apps.users.serializers import UserSerializer


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.annotate(work_time=Sum(F('timelog__end_time') - F('timelog__start_time')))
    serializer_class = TaskSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == 'create':
            return TaskCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, is_completed=False)

    def destroy(self, request, *args, **kwargs):
        task = get_object_or_404(Task.objects.filter(pk=kwargs.get('pk')))
        task.delete()
        return Response({"success": True, "message": "task deleted successfully"})

    def list(self, request, *args, **kwargs):
        tasks = Task.objects.annotate(work_time=Sum(F('timelog__end_time') - F('timelog__start_time')))
        return Response(TaskSerializer(tasks, many=True).data)

        # def get_work_time(self, instance):
        #     work_time = Task.objects.annotate(
        #         total=Sum(F('timelog__end_time') - F('timelog__start_time')))
        #     return work_time

    @action(methods=['GET'], detail=False, serializer_class=TasksInfoSerializer)
    def my(self, request):
        tasks = Task.objects.filter(owner=self.request.user)
        return Response(TasksInfoSerializer(tasks, many=True).data)

    @action(methods=['GET'], detail=False, serializer_class=TasksInfoSerializer)
    def completed(self, request):
        tasks = Task.objects.filter(is_completed=True)
        return Response(TasksInfoSerializer(tasks, many=True).data)

    @action(methods=['PATCH'], detail=True, serializer_class=TaskUpdateSerializer, url_path="update-owner")
    def update_owner(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        serializer = TaskUpdateSerializer(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        subject = 'A new task was assigned to you!'
        message = 'Hello, ' + task.owner.last_name + '\n' + task.title + ' was assigned to you. Go and check it out!'
        to_email = task.owner.email
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [to_email])

        return Response({"success": True, "message": "owner updated successfully"})

    @action(methods=['PATCH'], detail=True, serializer_class=TaskUpdateStatusSerializer, url_path="update-status")
    def update_status(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        serializer = TaskUpdateStatusSerializer(instance=task, data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        task_completed = validated_data.get('is_completed')
        serializer.save()
        if task.comment_set.exists():
            if task_completed is True:
                subject = 'One of your commented task has been completed!'
                message = 'Hello, ' + task.owner.last_name + '\n' + task.title + ' is done. Congratulations!'
                to_email = task.owner.email
                send_mail(subject, message, DEFAULT_FROM_EMAIL, [to_email])

        return Response({"success": True, "message": "status updated successfully"})


class UserListView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        users = USER_MODEL.objects.all()
        return Response(UserSerializer(users, many=True).data)


class TaskItemView(GenericAPIView):
    serializer_class = TaskItemSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        return Response(TaskItemSerializer(task).data)


class TaskItemLogsView(GenericAPIView):
    serializer_class = TaskItemLogsSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.filter(pk=pk))
        return Response(TaskItemLogsSerializer(task).data)


class TaskListViewWithWorktime(GenericAPIView):
    serializer_class = TaskItemLogsSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        task = Task.objects.all()
        return Response(TaskItemLogsSerializer(task).data)


class TaskSearchView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

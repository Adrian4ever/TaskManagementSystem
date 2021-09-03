from rest_framework import serializers

from apps.tasks.models import Task, UserTasks


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class TaskSerializerNoOwner(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description", "status")


class TasksAssignedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title")


class UserTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTasks
        fields = '__all__'

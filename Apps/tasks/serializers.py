from rest_framework import serializers

from apps.comments.serializers import CommentsSerializer
from apps.tasks.models import Task, UserTasks
from apps.timelogs.serializers import TimelogSerializer


class TaskSerializer(serializers.ModelSerializer):
    work_time = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'is_completed', 'owner', 'work_time')

    def get_work_time(self, obj):
        if obj.work_time:
            return obj.work_time/60
        return obj.work_time


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = ("owner", "is_completed")


class TasksInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title")


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("owner",)


class TaskUpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("is_completed",)


class UserTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTasks
        fields = '__all__'


class TaskItemSerializer(serializers.ModelSerializer):
    comment_list = CommentsSerializer(source='comment_set', read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'


class TaskItemLogsSerializer(serializers.ModelSerializer):
    timelog_list = TimelogSerializer(source='timelog_set', read_only=True, many=True)

    class Meta:
        model = Task
        fields = '__all__'

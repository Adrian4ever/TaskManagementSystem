from datetime import datetime

import pytz
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.timelogs.models import TimeLog
from apps.timelogs.serializers import TimelogSerializer, TimelogStartTimeSerializer, TimelogEndTimeSerializer


class TimeLogViewSet(ModelViewSet):
    queryset = TimeLog.objects.all()
    serializer_class = TimelogSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TimelogSerializer
        return super().get_serializer_class()

    @action(methods=['post'], detail=False, serializer_class=TimelogStartTimeSerializer)
    def start(self, request):
        serializer = TimelogStartTimeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        current_time = timezone.now()
        serializer.save(start_time=current_time)
        return Response({"success": True, "message": "timer has been successfully started"})

    @action(methods=['post'], detail=False, serializer_class=TimelogEndTimeSerializer)
    def stop(self, request):
        if TimeLog.objects.filter(end_time__isnull=True):
            last_timelog_list = TimeLog.objects.filter(end_time__isnull=True).order_by('start_time').first()
            last_timelog = get_object_or_404(TimeLog.objects.filter(pk=last_timelog_list.pk))
            serializer = TimelogEndTimeSerializer(instance=last_timelog, data=request.data)
            serializer.is_valid(raise_exception=True)
            current_time = timezone.now()
            serializer.save(end_time=current_time)
            return Response({"success": True, "message": "timer has been successfully stopped"})
        return Response({"success": False, "message": "there is no any started log to the given task id"})

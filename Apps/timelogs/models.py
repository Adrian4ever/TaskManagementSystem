from django.db import models
from django.utils import timezone

from apps.tasks.models import Task


class TimeLog(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

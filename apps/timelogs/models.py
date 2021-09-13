from django.db import models
from django.utils import timezone

from apps.tasks.models import Task
from apps.users.get_user_model import USER_MODEL


class TimeLog(models.Model):
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_index=True)
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE, db_index=True)

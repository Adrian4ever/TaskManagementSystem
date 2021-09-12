from django.db import models

from apps.users.get_user_model import USER_MODEL


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(USER_MODEL, on_delete=models.CASCADE)

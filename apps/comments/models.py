from django.db import models

from apps.tasks.models import Task


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, db_index=True)
    text = models.TextField()

# Generated by Django 3.2.7 on 2021-09-08 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_rename_iscompleted_task_is_completed'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='work_time',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
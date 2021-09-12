import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.tasks.models import Task
from apps.timelogs.models import TimeLog

faker = Faker()


class Command(BaseCommand):
    help = 'Generate fake Timelogs, default amount is 10'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The amount of fake data you want to generate')

    def handle(self, *args, **options):
        amount = options.get('amount', 10)
        count = 0
        for _ in range(amount):
            random_task = random.choice(Task.objects.all())
            timelog = TimeLog.objects.create(
                start_time=faker.past_datetime(),
                end_time=faker.future_datetime(),
                task=random_task,
                owner=random_task.owner
            )
            count += 1
            print('Timelog for task: ' + str(timelog.task.title) + '              generated: ' + str(count))
        print('Succesfully generated ' + str(count) + ' timelogs')

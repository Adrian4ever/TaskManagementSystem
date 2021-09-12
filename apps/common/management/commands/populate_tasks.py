import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.tasks.models import Task
from apps.users.get_user_model import USER_MODEL

faker = Faker()


class Command(BaseCommand):
    help = 'Generate fake tasks, default amount is 10'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The amount of fake data you want to generate')

    def handle(self, *args, **options):
        amount = options.get('amount', 10)
        count = 0
        for _ in range(amount):
            task = Task.objects.create(
                title=faker.word(),
                description=faker.text(),
                is_completed=faker.boolean(),
                owner=random.choice(USER_MODEL.objects.all())
            )
            count += 1
            print('Task: ' + str(task.title) + '              generated: ' + str(count))
        print('Succesfully generated ' + str(count) + ' tasks')

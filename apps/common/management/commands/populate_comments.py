import random

from django.core.management.base import BaseCommand
from faker import Faker

from apps.comments.models import Comment
from apps.tasks.models import Task

faker = Faker()


class Command(BaseCommand):
    help = 'Generate fake comments, default amount is 10'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The amount of fake data you want to generate')

    def handle(self, *args, **options):
        amount = options.get('amount', 10)
        count = 0
        for _ in range(amount):
            comment = Comment.objects.create(
                task=random.choice(Task.objects.all()),
                text=faker.text(),
            )
            count += 1
            print('Comment: ' + str(comment.text) + '              generated: ' + str(count))
        print('Succesfully generated ' + str(count) + ' comments')

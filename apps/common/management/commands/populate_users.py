from django.core.management.base import BaseCommand
from faker import Faker

from apps.users.get_user_model import USER_MODEL

faker = Faker()


class Command(BaseCommand):
    help = 'Generate fake data and seed models with them, default amount is 10'

    def add_arguments(self, parser):
        parser.add_argument('--amount', type=int, help='The amount of fake data you want to generate')

    def handle(self, *args, **options):
        amount = options.get('amount', 10)
        count = 0

        for _ in range(amount):
            user = USER_MODEL(
                first_name=faker.first_name(),
                last_name=faker.last_name(),
                email=faker.unique.email(),
            )
            user.set_password(faker.password())
            user.save()
            count += 1
            print(str(user) + '              generated: ' + str(count))

        print('Succesfully generated ' + str(count) + ' users')

from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from apps.users.get_user_model import USER_MODEL

faker = Faker()


class TestComment(APITestCase):
    queryset = USER_MODEL.objects.all()

    fixtures = [
        'users',
    ]

    def setUp(self) -> None:
        self.user = USER_MODEL.objects.first()
        self.client.force_authenticate(self.user)

    def test_register(self):
        fake_data = {
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "email": faker.email(),
            "password": faker.password(),

        }
        response = self.client.post(reverse('token_register'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_auth(self):
        fake_data = {
            "email": 'adrianursu121@gmail.com',
            "password": 'admin',
        }
        response = self.client.post(reverse('token_obtain_pair'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

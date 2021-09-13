import random

from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from apps.tasks.models import Task
from apps.timelogs.models import TimeLog
from apps.users.get_user_model import USER_MODEL

faker = Faker()

timelog_fake_data = {
    "start_time": faker.date_time_this_year(),
    "end_time": faker.date_time_this_year(),
    "task": random.choice(Task.objects.all()).id,
    "owner": random.choice(USER_MODEL.objects.all()).id
}
random_id = random.choice(TimeLog.objects.all()).id


class TestTimelog(APITestCase):
    queryset = TimeLog.objects.all()
    fixtures = [
        'users',
        'tasks',
        'timelogs'
    ]

    def setUp(self) -> None:
        self.user = USER_MODEL.objects.filter(email='adrianursu121@gmail.com').first()
        self.client.force_authenticate(self.user)

    def test_get(self):
        response = self.client.get(reverse('timelogs-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_my(self):
        response = self.client.get(reverse('timelogs-my'))
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        response = self.client.get(reverse('timelogs-detail', args=(random_id,)))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse('timelogs-list'), data=timelog_fake_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_post_start(self):
        fake_data = {
            "task": random.choice(Task.objects.all()).id
        }
        response = self.client.post(reverse('timelogs-start'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_post_end(self):
        fake_data = {
            "task": random.choice(Task.objects.all()).id
        }
        response = self.client.post(reverse('timelogs-stop'), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.delete(reverse('timelogs-detail', args=(random_id,)))
        self.assertEqual(self.queryset.filter(pk=random_id).count(), 0)

    def test_put(self):
        response = self.client.put(reverse('timelogs-detail', args=(random_id,)), data=timelog_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.client.patch(reverse('timelogs-detail', args=(random_id,)), data=timelog_fake_data,
                                     format='json')
        self.assertEqual(response.status_code, 200)

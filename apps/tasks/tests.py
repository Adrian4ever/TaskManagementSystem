import random

from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from apps.tasks.models import Task
from apps.users.get_user_model import USER_MODEL

faker = Faker()

task_fake_data = {
    "title": faker.word(),
    "description": faker.text(),
    "is_completed": faker.boolean(),
    "owner": random.choice(USER_MODEL.objects.all()).id
}
random_id = random.choice(Task.objects.all()).id
random_title = random.choice(Task.objects.all()).title


class TestTask(APITestCase):
    queryset = Task.objects.all()

    fixtures = [
        'users',
        'tasks'
    ]

    def setUp(self) -> None:
        self.user = USER_MODEL.objects.filter(email='adrianursu121@gmail.com').first()
        self.client.force_authenticate(self.user)

    def test_get(self):
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse('tasks-list'), data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_completed(self):
        response = self.client.get(reverse('tasks-completed'))
        self.assertEqual(response.status_code, 200)

    def test_get_my(self):
        response = self.client.get(reverse('tasks-my'))
        self.assertEqual(response.status_code, 200)

    def test_get_search(self):
        response = self.client.get(reverse('task-search'), params=(random_title,))
        self.assertEqual(response.status_code, 200)

    def test_get_top_20(self):
        response = self.client.get(reverse('tasks-top-20'))
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        response = self.client.get(reverse('tasks-detail', args=(random_id,)))
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.client.delete(reverse('tasks-detail', args=(random_id,)))
        self.assertEqual(self.queryset.filter(pk=random_id).count(), 0)

    def test_put(self):
        response = self.client.put(reverse('tasks-detail', args=(random_id,)), data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.client.patch(reverse('tasks-detail', args=(random_id,)), data=task_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_task_comments(self):
        response = self.client.get(reverse('task-comments', args=(random_id,)))
        self.assertEqual(response.status_code, 200)

    def test_get_task_logs(self):
        response = self.client.get(reverse('task-logs', args=(random_id,)))
        self.assertEqual(response.status_code, 200)

    def test_patch_owner(self):
        fake_data = {
            "owner": random.choice(USER_MODEL.objects.all()).id
        }
        response = self.client.patch(reverse('tasks-update-owner', args=(random_id,)), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch_status(self):
        fake_data = {
            "is_completed": faker.boolean()
        }
        response = self.client.patch(reverse('tasks-update-status', args=(random_id,)), data=fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_get_users(self):
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_user_logtime(self):
        response = self.client.get(reverse('user_logtime'))
        self.assertEqual(response.status_code, 200)

import random

from django.urls import reverse
from faker import Faker
from rest_framework.test import APITestCase

from apps.comments.models import Comment
from apps.tasks.models import Task
from apps.users.get_user_model import USER_MODEL

faker = Faker()

comment_fake_data = {
    "task": random.choice(Task.objects.all()).id,
    "text": faker.text(),
}
random_id = random.choice(Comment.objects.all()).id


class TestComment(APITestCase):
    queryset = Comment.objects.all()

    fixtures = [
        'users',
        'tasks',
        'comments'
    ]

    def setUp(self) -> None:
        self.user = USER_MODEL.objects.filter(email='test@test.com').first()
        self.client.force_authenticate(self.user)

    def test_get(self):
        response = self.client.get(reverse('comments-list'))
        self.assertEqual(response.status_code, 200)

    def test_get_by_pk(self):
        response = self.client.get(reverse('comments-detail', args=(random_id,)))
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.client.post(reverse('comments-list'), data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        self.client.delete(reverse('comments-detail', args=(random_id,)))
        self.assertEqual(self.queryset.filter(pk=random_id).count(), 0)

    def test_put(self):
        response = self.client.put(reverse('comments-detail', args=(random_id,)), data=comment_fake_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.client.patch(reverse('comments-detail', args=(random_id,)), data=comment_fake_data,
                                     format='json')
        self.assertEqual(response.status_code, 200)

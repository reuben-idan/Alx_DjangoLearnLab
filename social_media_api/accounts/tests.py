from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token


class FollowUnfollowTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username="alice", password="pass12345")
        self.user2 = User.objects.create_user(username="bob", password="pass12345")
        self.token1, _ = Token.objects.get_or_create(user=self.user1)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token1.key}")

    def test_follow_user(self):
        url = reverse('follow-user', args=[self.user2.id])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        # user1 now follows user2
        self.assertTrue(self.user2 in self.user1.following.all())
        # user2 has user1 as follower
        self.assertTrue(self.user1 in self.user2.followers.all())

    def test_unfollow_user(self):
        # First follow
        self.user1.following.add(self.user2)
        url = reverse('unfollow-user', args=[self.user2.id])
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(self.user2 in self.user1.following.all())

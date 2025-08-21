from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Post
from notifications.models import Notification


class FeedViewTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.alice = User.objects.create_user(username="alice", password="pass12345")
        self.bob = User.objects.create_user(username="bob", password="pass12345")
        self.carla = User.objects.create_user(username="carla", password="pass12345")

        # Alice follows Bob, not Carla
        self.alice.following.add(self.bob)

        # Create posts
        self.p1 = Post.objects.create(author=self.bob, title="Bob 1", content="...")
        self.p2 = Post.objects.create(author=self.bob, title="Bob 2", content="...")
        self.p3 = Post.objects.create(author=self.carla, title="Carla 1", content="...")

        token, _ = Token.objects.get_or_create(user=self.alice)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_feed_shows_followed_users_posts_only(self):
        url = reverse('feed')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        titles = [item['title'] for item in resp.data['results']]
        # Should include Bob's posts, exclude Carla's
        self.assertIn("Bob 1", titles)
        self.assertIn("Bob 2", titles)
        self.assertNotIn("Carla 1", titles)

    def test_feed_ordering_newest_first(self):
        url = reverse('feed')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        titles = [item['title'] for item in resp.data['results']]
        # Bob 2 created after Bob 1, so it should appear first
        self.assertTrue(titles.index("Bob 2") < titles.index("Bob 1"))


class LikeTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.author = User.objects.create_user(username="author", password="pass12345")
        self.liker = User.objects.create_user(username="liker", password="pass12345")
        self.post = Post.objects.create(author=self.author, title="A", content="B")
        token, _ = Token.objects.get_or_create(user=self.liker)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_like_creates_notification_and_is_idempotent(self):
        url = reverse('post-like', args=[self.post.id])
        r1 = self.client.post(url)
        self.assertEqual(r1.status_code, 200)
        notif = Notification.objects.filter(recipient=self.author, actor=self.liker, verb__icontains='liked').first()
        self.assertIsNotNone(notif)
        # Second like should not duplicate
        r2 = self.client.post(url)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(Notification.objects.filter(recipient=self.author, actor=self.liker, verb__icontains='liked').count(), 1)

    def test_unlike(self):
        like_url = reverse('post-like', args=[self.post.id])
        unlike_url = reverse('post-unlike', args=[self.post.id])
        self.client.post(like_url)
        r = self.client.post(unlike_url)
        self.assertEqual(r.status_code, 200)

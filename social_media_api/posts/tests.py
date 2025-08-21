from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from .models import Post


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

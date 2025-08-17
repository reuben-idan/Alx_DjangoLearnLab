from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.conf import settings

User = get_user_model()

class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_registration(self):
        """Test user registration with valid data."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_rate_limiting(self):
        """Test login rate limiting after multiple failed attempts."""
        for _ in range(5):
            response = self.client.post(reverse('login'), {
                'username': 'wronguser',
                'password': 'wrongpass',
            })
        # 6th attempt should be rate limited
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpass',
        })
        self.assertEqual(response.status_code, 429)

    def test_email_verification_flow(self):
        """Test the email verification process."""
        # Create unverified user
        user = User.objects.create_user(
            username='unverified',
            email='unverified@example.com',
            password='testpass123',
            is_active=False
        )
        
        # Simulate email verification
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        response = self.client.get(
            reverse('verify-email', kwargs={'uidb64': uid, 'token': token})
        )
        user.refresh_from_db()
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, 302)

    def test_profile_update(self):
        """Test user profile update functionality."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'bio': 'New bio',
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.bio, 'New bio')
        self.assertEqual(response.status_code, 302)

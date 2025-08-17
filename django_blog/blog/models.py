from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

class Profile(models.Model):
    """
    Extends the default User model with additional profile information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, help_text="A short bio about the user")
    location = models.CharField(max_length=100, blank=True, help_text="User's location")
    birth_date = models.DateField(null=True, blank=True, help_text="User's date of birth")
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True, help_text="User's profile picture")
    website = models.URLField(max_length=200, blank=True, help_text="User's personal website")
    
    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile for each new user."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile when the user is saved."""
    instance.profile.save()

class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200, help_text="Enter the title of the blog post")
    content = models.TextField(help_text="Enter the content of the blog post")
    published_date = models.DateTimeField(auto_now_add=True, help_text="The date and time when the post was published")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', help_text="The user who created this post")
    updated_at = models.DateTimeField(auto_now=True, help_text="The date and time when the post was last updated")

    class Meta:
        ordering = ['-published_date']
        permissions = [
            ('can_publish', 'Can publish posts'),
            ('can_edit_any_post', 'Can edit any post'),
            ('can_delete_any_post', 'Can delete any post'),
        ]

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title} by {self.author.username}"

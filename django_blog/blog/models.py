from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    """
    Model representing a blog post.
    """
    title = models.CharField(max_length=200, help_text="Enter the title of the blog post")
    content = models.TextField(help_text="Enter the content of the blog post")
    published_date = models.DateTimeField(auto_now_add=True, help_text="The date and time when the post was published")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', help_text="The user who created this post")

    class Meta:
        ordering = ['-published_date']

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title} by {self.author.username}"

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from taggit.managers import TaggableManager

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
    Model representing a blog post with content, author, and publishing information.
    """
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="Enter a descriptive title for your blog post"
    )
    slug = models.SlugField(
        max_length=250,
        unique_for_date='published_date',
        help_text="A URL-friendly version of the title (auto-generated)"
    )
    content = models.TextField(
        help_text="The main content of your blog post (markdown supported)"
    )
    excerpt = models.TextField(
        max_length=500,
        blank=True,
        help_text="A short summary of the post (optional, first 500 chars will be used if blank)"
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Set to 'published' to make this post publicly visible"
    )
    published_date = models.DateTimeField(
        default=timezone.now,
        help_text="The date and time when the post was published"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        help_text="The user who created this post"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the post was last updated"
    )
    featured_image = models.ImageField(
        upload_to='blog_images/',
        blank=True,
        null=True,
        help_text="Featured image for the blog post"
    )
    allow_comments = models.BooleanField(
        default=True,
        help_text="Allow comments on this post"
    )
    view_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Number of times this post has been viewed"
    )
    
    # Tags for the post
    tags = TaggableManager(
        blank=True,
        help_text="A comma-separated list of tags",
        verbose_name="Tags"
    )

    class Meta:
        ordering = ['-published_date']
        permissions = [
            ('can_publish', 'Can publish posts'),
            ('can_edit_any_post', 'Can edit any post'),
            ('can_delete_any_post', 'Can delete any post'),
        ]
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'

    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        """
        Override save to set slug and excerpt if not provided.
        """
        from django.utils.text import slugify
        from django.utils.html import strip_tags
        
        if not self.slug:
            self.slug = slugify(self.title)
            
        if not self.excerpt and self.content:
            # Create excerpt from first 500 chars of content (without HTML tags)
            plain_text = strip_tags(self.content)
            self.excerpt = plain_text[:500]
            
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        """
        Returns the canonical URL for the post.
        """
        from django.urls import reverse
        return reverse('post_detail', args=[
            self.published_date.year,
            self.published_date.month,
            self.published_date.day,
            self.slug
        ])
        
    def increment_view_count(self):
        """Increment the view count for this post."""
        self.view_count += 1
        self.save(update_fields=['view_count'])
        
    def can_edit(self, user):
        """Check if a user can edit this post."""
        return user == self.author or user.has_perm('blog.can_edit_any_post')
        
    def can_delete(self, user):
        """Check if a user can delete this post."""
        return user == self.author or user.has_perm('blog.can_delete_any_post')
        
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title} by {self.author.username}"


class Comment(models.Model):
    """
    Model representing comments on blog posts.
    """
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The blog post this comment belongs to"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text="The user who created this comment"
    )
    content = models.TextField(
        max_length=1000,
        help_text="The content of the comment"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the comment was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the comment was last updated"
    )
    active = models.BooleanField(
        default=True,
        help_text="Set to False to hide this comment (soft delete)"
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies',
        help_text="Parent comment if this is a reply"
    )

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'
        permissions = [
            ('can_moderate', 'Can moderate comments (approve/reject)'),
        ]

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    def can_edit(self, user):
        """Check if a user can edit this comment."""
        return user == self.author or user.has_perm('blog.can_moderate')
    
    def can_delete(self, user):
        """Check if a user can delete this comment."""
        return user == self.author or user.has_perm('blog.can_moderate')
    
    def get_absolute_url(self):
        """Return URL to the comment's post with fragment identifier."""
        return f"{self.post.get_absolute_url()}#comment-{self.id}"

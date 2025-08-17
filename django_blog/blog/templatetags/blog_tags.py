from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()

@register.simple_tag
def total_posts():
    """Returns the total number of published posts."""
    return Post.published.count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    """Displays the latest published posts."""
    latest_posts = Post.published.order_by('-published_date')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    """Returns the most commented posts."""
    return Post.published.annotate(
        total_comments=Count('comments')
    ).filter(total_comments__gt=0).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    """Converts markdown text to HTML."""
    return mark_safe(markdown.markdown(text, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ]))

@register.simple_tag
def get_popular_tags(count=10):
    """Returns the most popular tags."""
    return Post.tags.most_common()[:count]

from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'status')
    list_filter = ('status', 'published_date', 'author', 'tags')
    search_fields = ('title', 'content', 'tags__name')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date', 'author')
    filter_horizontal = ('tags',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'author', 'content', 'excerpt', 'status', 'featured_image')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('published_date', 'allow_comments', 'tags'),
        }),
    )

admin.site.register(Post, PostAdmin)

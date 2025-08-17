from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Post

# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    list_filter = ('published_date', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date', 'author')

admin.site.register(Post, PostAdmin)

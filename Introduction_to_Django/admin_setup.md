# Django Admin Interface Setup

## Overview

The Django admin interface has been configured for the Book model to provide efficient data management capabilities.

## Admin Configuration

### Book Model Registration

The Book model is registered with the Django admin interface using the `@admin.register(Book)` decorator.

### Admin Customization

The `BookAdmin` class provides the following customizations:

- **List Display**: Shows title, author, and publication_year in the admin list view
- **List Filters**: Filters by publication_year and author
- **Search Fields**: Search functionality for title and author fields
- **Ordering**: Books are ordered alphabetically by title

## Access Information

### Admin URL

- **Admin Interface**: http://127.0.0.1:8000/admin/

### Superuser Credentials

- **Username**: admin
- **Email**: admin@example.com
- **Password**: (set during creation)

## Features Available

1. **Book Management**: Create, read, update, and delete book records
2. **Filtering**: Filter books by publication year or author
3. **Search**: Search books by title or author
4. **Sorting**: Sort books alphabetically by title
5. **Bulk Operations**: Select multiple books for bulk operations

## Usage Instructions

1. Start the development server: `python manage.py runserver`
2. Navigate to http://127.0.0.1:8000/admin/
3. Log in with the superuser credentials
4. Click on "Books" to manage book records
5. Use the filters and search functionality to find specific books
6. Add, edit, or delete books as needed

## Code Implementation

```python
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
    ordering = ('title',)
```

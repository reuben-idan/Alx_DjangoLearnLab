from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Author, Book, Library, Librarian, UserProfile

# Register your models here.

class CustomUserAdmin(UserAdmin):
    """
    Custom admin configuration for CustomUser model.
    """
    # Fields to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    # Fields to display in the user detail/edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    # Make profile_photo field readonly in the list view for better performance
    readonly_fields = ('date_joined', 'last_login')


class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for UserProfile model.
    """
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
    

class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for Author model.
    """
    list_display = ('name',)
    search_fields = ('name',)


class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for Book model.
    """
    list_display = ('title', 'author')
    list_filter = ('author',)
    search_fields = ('title', 'author__name')


class LibraryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Library model.
    """
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('books',)


class LibrarianAdmin(admin.ModelAdmin):
    """
    Admin configuration for Librarian model.
    """
    list_display = ('name', 'library')
    search_fields = ('name', 'library__name')


# Register models with their respective admin classes
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Library, LibraryAdmin)
admin.site.register(Librarian, LibrarianAdmin)

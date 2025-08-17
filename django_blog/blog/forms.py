from django import forms
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from taggit.forms import TagWidget
from .models import Post, Profile, Comment
from taggit.models import Tag

class UserRegisterForm(UserCreationForm):
    """Form for user registration with email and password validation."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email address')
        })
    )
    username = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Choose a username')
        })
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Create a password')
        }),
        help_text=_("Your password must contain at least 8 characters.")
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm your password')
        }),
        help_text=_("Enter the same password as before, for verification.")
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("This email is already in use. Please use a different email address."),
                code='email_exists'
            )
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError(
                _("This username is already taken. Please choose another."),
                code='username_exists'
            )
        return username

class UserLoginForm(AuthenticationForm):
    """Form for user login with email/username and password."""
    username = forms.CharField(
        label=_("Email or Username"),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email or username')
        })
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your password')
        })
    )

class UserUpdateForm(forms.ModelForm):
    """Form for updating user information."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your email address')
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError(
                _("This email is already in use. Please use a different email address."),
                code='email_exists'
            )
        return email

class ProfileUpdateForm(forms.ModelForm):
    """Form for updating user profile information."""
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'website', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': _('Tell us about yourself...')
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Your location')
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'website': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com'
            }),
        }

class CustomPasswordChangeForm(PasswordChangeForm):
    """Form for changing user password with custom styling."""
    old_password = forms.CharField(
        label=_("Current password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter your current password')
        })
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Enter new password')
        }),
        help_text=_("Your password must contain at least 8 characters.")
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Confirm new password')
        })
    )

class PostForm(forms.ModelForm):
    """Form for creating and updating blog posts."""
    tags = forms.CharField(
        widget=TagWidget(),
        required=False,
        help_text='Add tags to categorize your post (separate with commas)'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'featured_image', 'allow_comments', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a title for your post'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your blog post here...', 'rows': 10}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'allow_comments': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        help_texts = {
            'title': _('A clear and descriptive title for your post'),
            'content': _('The main content of your blog post (markdown supported)'),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError(_('Title must be at least 5 characters long.'))
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 50:
            raise forms.ValidationError(_('Content must be at least 50 characters long.'))
        return content

class SearchForm(forms.Form):
    """Form for searching blog posts."""
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search posts...',
            'aria-label': 'Search'
        })
    )
    tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        empty_label='All Tags',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'aria-label': 'Filter by tag'
        })
    )

    def search(self):
        """
        Perform the search based on form data.
        Returns a queryset of matching posts.
        """
        queryset = Post.published.all()
        query = self.cleaned_data.get('query')
        tag = self.cleaned_data.get('tag')

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        
        if tag:
            queryset = queryset.filter(tags__in=[tag])
            
        return queryset
        return queryset.distinct()


class CommentForm(forms.ModelForm):
    """
    Form for creating and updating comments.
    """
    class Meta:
        model = Comment
        fields = ['content', 'parent']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10,
                'placeholder': _('Write your post content here...')
            }),
        }

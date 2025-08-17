import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView, View
from django.db.models import Q
from taggit.models import Tag
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.views.generic import CreateView, TemplateView, FormView, UpdateView, DeleteView, ListView, DetailView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import Post, Profile, Comment
from .forms import (
    UserRegisterForm, PostForm, UserLoginForm, 
    UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm,
    CommentForm, SearchForm
)

# Blog post views
class PostListView(ListView):
    """View for displaying a list of blog posts."""
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """Return only published posts for non-staff users."""
        queryset = Post.objects.filter(status='published')
        if self.request.user.is_staff:
            queryset = Post.objects.all()
        return queryset.order_by('-published_date')

class PostDetailView(DetailView):
    """View for displaying a single blog post."""
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Only show published posts to non-staff users."""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        return queryset
    
    def get(self, request, *args, **kwargs):
        """Increment view count when post is viewed."""
        response = super().get(request, *args, **kwargs)
        if self.object.status == 'published':
            self.object.increment_view_count()
        return response

class PostCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new blog post."""
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    login_url = 'login'
    
    def form_valid(self, form):
        """Set the author to the current user and handle published status."""
        form.instance.author = self.request.user
        
        # Check if user has permission to publish
        if not self.request.user.has_perm('blog.can_publish'):
            form.instance.status = 'draft'
            
        messages.success(self.request, _('Your post has been created!'))
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the created post."""
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing blog post."""
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'  # Updated template path
    login_url = 'login'
    permission_denied_message = "You don't have permission to edit this post."
    
    def test_func(self):
        """Only allow the author or users with edit permission to update."""
        post = self.get_object()
        return post.can_edit(self.request.user)
    
    def form_valid(self, form):
        """Set the updated timestamp."""
        messages.success(self.request, _('Your post has been updated!'))
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the updated post."""
        return reverse('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a blog post."""
    model = Post
    template_name = 'post_confirm_delete.html'  # Updated template path
    success_url = reverse_lazy('post_list')
    login_url = 'login'
    permission_denied_message = "You don't have permission to delete this post."
    
    def test_func(self):
        """Only allow the author or users with delete permission to delete."""
        post = self.get_object()
        return post.can_delete(self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """Show success message after deletion."""
        messages.success(request, _('Your post has been deleted!'))
        return super().delete(request, *args, **kwargs)

class UserLoginView(LoginView):
    """View for user login with rate limiting."""
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    @method_decorator(ratelimit(key='post:username', rate='5/m', method='POST', block=True))
    @method_decorator(never_cache)
    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

class UserLogoutView(LogoutView):
    """View for user logout."""
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You have been successfully logged out."))
        return super().dispatch(request, *args, **kwargs)

class SignUpView(FormView):
    """View for user registration with email verification."""
    form_class = UserRegisterForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Create user but don't save yet
        user = form.save(commit=False)
        user.is_active = False  # User inactive until email verification
        user.save()
        
        # Send verification email
        self.send_verification_email(user, form.cleaned_data.get('email'))
        
        messages.info(
            self.request,
            'Please check your email to complete registration.'
        )
        return super().form_valid(form)
    
    def send_verification_email(self, user, to_email):
        """Send email with verification link."""
        mail_subject = 'Verify your email address'
        message = render_to_string('emails/verify_email.html', {
            'user': user,
            'domain': get_current_site(self.request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'protocol': 'https' if self.request.is_secure() else 'http',
        })
        send_mail(mail_subject, message, None, [to_email])

class VerifyEmailView(View):
    """View to handle email verification."""
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'Your email has been verified! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'The verification link is invalid or has expired.')
            return redirect('signup')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(
            self.request, 
            _('Welcome, %(username)s! Your account has been created successfully.') % {'username': user.username}
        )
        return super().form_valid(form)

@login_required
def profile(request):
    """View for user profile."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _('Your profile has been updated!'))
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'title': _('Profile')
    }
    return render(request, 'registration/profile.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    """View for changing password."""
    form_class = CustomPasswordChangeForm
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        messages.success(
            self.request, 
            _('Your password has been changed successfully!')
        )
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)

class CustomPasswordResetView(PasswordResetView):
    """View for requesting a password reset."""
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    template_name = 'registration/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """View for setting a new password after reset."""
    form_class = SetPasswordForm
    template_name = 'registration/password_reset_complete.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        messages.success(
            _('Your password has been set. You may go ahead and log in now.')
        )
        return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin, CreateView):
    """View for creating a new comment on a post."""
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'  # Updated template path
    login_url = 'login'
    
    def form_valid(self, form):
        """Set the author to the current user and associate with the post."""
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        response = super().form_valid(form)
        messages.success(self.request, 'Your comment has been added!')
        return response
    
    def get_success_url(self):
        """Redirect back to the post detail page."""
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']}) + '#comments'


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating an existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'comment_form.html'  # Updated template path
    login_url = 'login'
    permission_denied_message = "You don't have permission to edit this comment."
    
    def test_func(self):
        """Only allow the comment author to update."""
        comment = self.get_object()
        return comment.author == self.request.user
    
    def form_valid(self, form):
        """Show success message after update."""
        messages.success(self.request, 'Your comment has been updated!')
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect back to the post detail page."""
        return reverse('post_detail', kwargs={'pk': self.object.post.pk}) + '#comments'


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """View for deleting a comment."""
    model = Comment
    template_name = 'comment_confirm_delete.html'  # Updated template path
    login_url = 'login'
    permission_denied_message = "You don't have permission to delete this comment."
    
    def test_func(self):
        """Only allow the comment author or post author to delete."""
        comment = self.get_object()
        return comment.author == self.request.user or comment.post.author == self.request.user
    
    def delete(self, request, *args, **kwargs):
        """Show success message after deletion."""
        messages.success(request, 'Your comment has been deleted!')
        return super().delete(request, *args, **kwargs)
    
    def get_success_url(self):
        """Redirect back to the post detail page."""
        return reverse('post_detail', kwargs={'pk': self.object.post.pk}) + '#comments'


class PostByTagListView(ListView):
    """View for displaying posts filtered by a specific tag."""
    model = Post
    template_name = 'posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """Return posts filtered by the specified tag."""
        tag_slug = self.kwargs.get('tag_slug')
        self.tag = get_object_or_404(Tag, slug=tag_slug)
        return Post.published.filter(tags__in=[self.tag]).distinct()
    
    def get_context_data(self, **kwargs):
        """Add the tag to the template context."""
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class PostSearchView(ListView):
    """View for searching blog posts."""
    model = Post
    template_name = 'post_search.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        """Return search results based on query parameters."""
        queryset = Post.published.all()
        query = self.request.GET.get('query')
        tag_slug = self.kwargs.get('tag_slug')
        
        # Search by query string
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        
        # Filter by tag if provided
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags__in=[tag])
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """Add search form, query, and selected tag to the context."""
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET or None)
        context['query'] = self.request.GET.get('query', '')
        
        # Add selected tag to context if present
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['tag'] = get_object_or_404(Tag, slug=tag_slug)
        
        context['selected_tag'] = self.request.GET.get('tag', '')
        return context


def about(request):
    """View for the about page."""
    return render(request, 'about.html', {'title': _('About')})

@login_required()
def delete_account(request):
    """View for deleting user account."""
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(
            request, 
            _('Your account has been deleted successfully.')
        )
        return redirect('home')
    return render(request, 'registration/account_confirm_delete.html')

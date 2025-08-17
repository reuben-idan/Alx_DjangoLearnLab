import os
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from .models import Post, Profile
from .forms import (
    UserRegisterForm, PostForm, UserLoginForm, 
    UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
)

class PostListView(ListView):
    model = Post
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been updated!')
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('home')
    success_message = 'Your post has been deleted!'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class UserLoginView(LoginView):
    """View for user login."""
    form_class = UserLoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            # Set session to expire when the user closes the browser
            self.request.session.set_expiry(0)
            # Set a long expiration for the session cookie
            self.request.session.modified = True
        return super().form_valid(form)

class UserLogoutView(LogoutView):
    """View for user logout."""
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You have been successfully logged out."))
        return super().dispatch(request, *args, **kwargs)

class SignUpView(FormView):
    """View for user registration."""
    form_class = UserRegisterForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

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
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

    def form_valid(self, form):
        messages.success(
            self.request, 
            _('Your password has been set. You may go ahead and log in now.')
        )
        return super().form_valid(form)

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

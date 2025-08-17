from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views
from .views import (
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    PostSearchView, PostByTagListView, SignUpView, profile, CustomLoginView
)

urlpatterns = [
    # Core URLs
    path('', views.home, name='blog-home'),
    path('home/', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:year>/<int:month>/<int:day>/<slug:slug>/', 
         views.PostDetailView.as_view(), 
         name='post_detail'),
    path('posts/<int:pk>/edit/', 
         views.PostUpdateView.as_view(), 
         name='post_update'),
    path('posts/<int:pk>/delete/', 
         views.PostDeleteView.as_view(), 
         name='post_confirm_delete'),
    path('post/<int:pk>/delete/', 
         views.PostDeleteView.as_view(), 
         name='post_delete'),
    path('post/<int:pk>/update/', 
         views.PostUpdateView.as_view(), 
         name='post_update_alt'),
    path('post/new/', 
         views.PostCreateView.as_view(), 
         name='post_create_alt'),
    
    # Authentication URLs
    path('accounts/', include([
        path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
        path('signup/', SignUpView.as_view(), name='signup'),
        path('profile/', profile, name='profile'),
        path('password_change/', auth_views.PasswordChangeView.as_view(
            template_name='registration/password_change_form.html',
            success_url='password_change_done'
        ), name='password_change'),
        path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='registration/password_change_done.html'
        ), name='password_change_done'),
        path('password_reset/', auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt',
            success_url='password_reset_done'
        ), name='password_reset'),
        path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html'
        ), name='password_reset_done'),
        path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='password_reset_complete'
        ), name='password_reset_confirm'),
        path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html'
        ), name='password_reset_complete'),
        path('verify-email/<uidb64>/<token>/', 
             views.VerifyEmailView.as_view(), 
             name='verify-email'),
        path('delete/', views.delete_account, name='delete_account'),
    ])),
    path('accounts/password/change/', 
         views.CustomPasswordChangeView.as_view(), 
         name='password_change'),
    path('accounts/password/change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ),
         name='password_change_done'),
    path('accounts/password/reset/', 
         views.CustomPasswordResetView.as_view(), 
         name='password_reset'),
    path('accounts/password/reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # Comment URLs
    path('posts/<int:post_id>/comments/new/',
         CommentCreateView.as_view(),
         name='comment_create'),
    path('post/<int:pk>/comments/new/',
         CommentCreateView.as_view(),
         name='comment_create_alt'),
    path('posts/<int:post_id>/comments/<int:comment_id>/edit/',
         CommentUpdateView.as_view(),
         name='comment_update'),
    path('comment/<int:pk>/update/',
         CommentUpdateView.as_view(),
         name='comment_update_alt'),
    path('posts/<int:post_id>/comments/<int:comment_id>/delete/',
         CommentDeleteView.as_view(),
         name='comment_delete'),
    path('comment/<int:pk>/delete/',
         CommentDeleteView.as_view(),
         name='comment_delete_alt'),
    
    # Search and Tag URLs
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('tags/<slug:tag_slug>/', PostByTagListView.as_view(), name='posts_by_tag'),
    
    # Password reset URLs
    path('password/reset/',
         views.CustomPasswordResetView.as_view(
             email_template_name='registration/password_reset_email.html',
             subject_template_name='registration/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password/reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password/reset/confirm/<uidb64>/<token>/',
         views.CustomPasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

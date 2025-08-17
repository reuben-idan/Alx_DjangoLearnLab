from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    # Core URLs
    path('', views.PostListView.as_view(), name='post_list'),
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
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
    path('accounts/verify-email/<uidb64>/<token>/', 
         views.VerifyEmailView.as_view(), 
         name='verify-email'),
    path('accounts/profile/', views.profile, name='profile'),
    path('accounts/delete/', views.delete_account, name='delete_account'),
    path('verify-email/<uidb64>/<token>/', 
         views.VerifyEmailView.as_view(), 
         name='verify-email'),
    path('profile/', views.profile, name='profile'),
    path('account/delete/', views.delete_account, name='delete_account'),
    
    # Password management URLs
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

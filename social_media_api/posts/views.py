from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination

class IsOwnerOrReadOnly(permissions.BasePermission):
    """Allow edits/deletes only to owners; read-only for others."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        owner = getattr(obj, 'author', None)
        return owner == request.user

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('post', 'author').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated & IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Create your views here.


class FeedView(generics.ListAPIView):
    """Aggregated feed of posts from users the request.user follows."""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_qs = getattr(user, 'following', None)
        if following_qs is None:
            return Post.objects.none()
        return (
            Post.objects.select_related('author')
            .filter(author__in=following_qs.all())
            .order_by('-created_at')
        )

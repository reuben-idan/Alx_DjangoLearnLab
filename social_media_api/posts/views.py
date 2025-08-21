from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from notifications.utils import create_notification

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
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content', 'author__username']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        from .models import Like
        obj, created = Like.objects.get_or_create(post=post, user=request.user)
        if created:
            # notify post author
            create_notification(recipient=post.author, actor=request.user, verb='liked your post', target=post)
            return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)
        return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = self.get_object()
        from .models import Like
        deleted, _ = Like.objects.filter(post=post, user=request.user).delete()
        if deleted:
            return Response({"detail": "Like removed."}, status=status.HTTP_200_OK)
        return Response({"detail": "You had not liked this post."}, status=status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('post', 'author').all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        # notify post author on comment
        create_notification(
            recipient=comment.post.author,
            actor=self.request.user,
            verb='commented on your post',
            target=comment.post,
        )

# Create your views here.


class FeedView(generics.ListAPIView):
    """Aggregated feed of posts from users the request.user follows."""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        try:
            following = self.request.user.following
            following_users = following.all()
        except AttributeError:
            return Post.objects.none()
        return Post.objects.filter(author__in=following_users).order_by('-created_at', '-id')

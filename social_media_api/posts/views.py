from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

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
        post = generics.get_object_or_404(Post, pk=pk)
        obj, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            # notify post author
            ct = ContentType.objects.get_for_model(Post)
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb='liked your post',
                target_content_type=ct,
                target_object_id=post.pk,
            )
            return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)
        return Response({"detail": "Already liked."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        post = generics.get_object_or_404(Post, pk=pk)
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
        ct = ContentType.objects.get_for_model(Post)
        Notification.objects.create(
            recipient=comment.post.author,
            actor=self.request.user,
            verb='commented on your post',
            target_content_type=ct,
            target_object_id=comment.post.pk,
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

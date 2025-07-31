from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """API endpoint that allows books to be viewed."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class BookViewSet(viewsets.ModelViewSet):
    """CRUD API endpoint for Book model."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

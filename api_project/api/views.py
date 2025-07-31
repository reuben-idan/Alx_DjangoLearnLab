from rest_framework import generics, viewsets

from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """API endpoint that allows books to be viewed."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """CRUD API endpoint for Book model."""

    queryset = Book.objects.all()
    serializer_class = BookSerializer

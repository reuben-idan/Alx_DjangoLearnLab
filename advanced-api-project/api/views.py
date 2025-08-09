from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows authors to be viewed or edited.
    """
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    """
    queryset = Book.objects.all().order_by('title')
    serializer_class = BookSerializer
    
    def get_queryset(self):
        """
        Optionally filter books by author ID if provided in the query parameters.
        """
        queryset = Book.objects.all().order_by('title')
        author_id = self.request.query_params.get('author_id')
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
        return queryset

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListView, DetailView, UpdateView, DeleteView, CreateView


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read permissions are allowed to any request.
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to admin users
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Assumes the model instance has an 'owner' attribute.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
            
        # Write permissions are only allowed to the owner of the object
        # In a real application, you would check if obj.owner == request.user
        # For this example, we'll just check if the user is authenticated
        return request.user and request.user.is_authenticated
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class BookCreateView(CreateView):
    """
    View for creating a new book.
    POST /books/create/ - Create a new book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    
    def perform_create(self, serializer):
        """Set additional data or perform actions before saving a new book."""
        book = serializer.save()
        print(f"New book created: {book.title} (ID: {book.id})")


class BookListView(ListView):
    """
    View for listing all books.
    GET /books/ - List all books
    """
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    
    def get_queryset(self):
        """
        Optionally filter books by author ID if provided in the query parameters.
        Also supports searching by title and filtering by publication year range.
        """
        queryset = Book.objects.all().order_by('title')
        
        # Filter by author_id if provided
        author_id = self.request.query_params.get('author_id')
        if author_id is not None:
            queryset = queryset.filter(author_id=author_id)
            
        # Search by title if provided
        title = self.request.query_params.get('title', '').strip()
        if title:
            queryset = queryset.filter(title__icontains=title)
            
        # Filter by publication year range if provided
        min_year = self.request.query_params.get('min_year')
        max_year = self.request.query_params.get('max_year')
        
        if min_year and min_year.isdigit():
            queryset = queryset.filter(publication_year__gte=int(min_year))
        if max_year and max_year.isdigit():
            queryset = queryset.filter(publication_year__lte=int(max_year))
            
        return queryset
    
    def perform_create(self, serializer):
        """
        Set the current user as the creator of the book and save.
        Also logs the creation of the book.
        """
        # In a real application, you might want to add the current user as a creator
        # if you have a user field in your Book model
        # serializer.save(created_by=self.request.user)
        
        # Log the creation (in a real app, you might use Django's logging)
        book = serializer.save()
        print(f"New book created: {book.title} (ID: {book.id})")
        
        # You could also send a signal or trigger an async task here
        # For example, to update search indices or send notifications


class BookDetailView(DetailView):
    """
    View for retrieving a specific book.
    GET /books/<id>/ - Retrieve a book
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'id'


class BookUpdateView(UpdateView):
    """
    View for updating a specific book.
    PUT /books/update/<id>/ - Update a book (requires authentication)
    PATCH /books/update/<id>/ - Partially update a book (requires authentication)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    lookup_field = 'id'
    
    def get_serializer_context(self):
        """Add the request to the serializer context."""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_update(self, serializer):
        """Handle book update with logging."""
        book = serializer.save()
        print(f"Book updated: {book.title} (ID: {book.id})")

    def update(self, request, *args, **kwargs):
        """Handle update with custom response."""
        response = super().update(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            response.data = {
                'message': 'Book updated successfully',
                'data': response.data
            }
        return response


class BookDeleteView(DeleteView):
    """
    View for deleting a specific book.
    DELETE /books/delete/<id>/ - Delete a book (requires admin)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'
    
    def get_serializer_context(self):
        """
        Add the request to the serializer context.
        This is useful if you need access to the request in the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_update(self, serializer):
        """
        Set additional data or perform actions before updating a book.
        In a real application, you might want to track who made the last update.
        """
        # In a real application, you might want to track who made the update
        # if hasattr(serializer.Meta.model, 'updated_by'):
        #     serializer.save(updated_by=self.request.user)
        # else:
        #     serializer.save()
        
        book = serializer.save()
        print(f"Book updated: {book.title} (ID: {book.id})")

    def update(self, request, *args, **kwargs):
        """
        Override update to add custom response and validation.
        """
        # You can add pre-update validation here
        # For example, check if the user has permission to update this specific book
        
        # Call the parent update method which will call perform_update
        response = super().update(request, *args, **kwargs)
        
        # Customize the response if needed
        if response.status_code == status.HTTP_200_OK:
            response.data = {
                'message': 'Book updated successfully',
                'data': response.data
            }
            
        return response

    def destroy(self, request, *args, **kwargs):
        """
        Handle book deletion with appropriate response and logging.
        """
        instance = self.get_object()
        book_id = instance.id
        book_title = instance.title
        
        # In a real application, you might want to check additional permissions here
        # or perform soft delete instead of hard delete
        
        self.perform_destroy(instance)
        
        # Log the deletion
        print(f"Book deleted: {book_title} (ID: {book_id})")
        
        return Response(
            {"message": f"Book '{book_title}' was deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


class AuthorViewSet(ListView, DetailView, UpdateView, DeleteView):
    """
    API endpoint that allows authors to be viewed or edited.
    GET /authors/ - List all authors
    POST /authors/ - Create a new author (requires authentication)
    GET /authors/<id>/ - Retrieve an author
    PUT/PATCH /authors/<id>/ - Update an author (requires authentication)
    DELETE /authors/<id>/ - Delete an author (requires authentication)
    """
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    lookup_field = 'id'

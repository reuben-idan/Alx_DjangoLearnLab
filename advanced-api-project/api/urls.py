from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browsable API.
urlpatterns = [
    # Book endpoints (kept as individual views for demonstration)
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:id>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/update/<int:id>/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/delete/<int:id>/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Include the router URLs
    path('', include(router.urls)),
    
    # API root
    path('', views.api_root, name='api-root'),
]

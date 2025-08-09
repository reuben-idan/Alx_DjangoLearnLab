from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    path('books/<int:id>/', views.BookDetailView.as_view(), name='book-detail'),
    path('books/<int:id>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('books/<int:id>/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Author endpoints (kept as ViewSet for simplicity, but can be split similarly if needed)
    path('authors/', views.AuthorViewSet.as_view({'get': 'list', 'post': 'create'}), name='author-list'),
    path('authors/<int:id>/', views.AuthorViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='author-detail'),
    
    # API root
    path('', views.api_root, name='api-root'),
]

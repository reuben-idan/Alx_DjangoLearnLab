from django.urls import path
from . import views

urlpatterns = [
    # Book endpoints
    path('books/', views.BookListCreateView.as_view(), name='book-list-create'),
    path('books/<int:id>/', views.BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
    
    # Author endpoints
    path('authors/', views.AuthorViewSet.as_view({'get': 'list', 'post': 'create'}), name='author-list-create'),
    path('authors/<int:id>/', views.AuthorViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='author-detail'),
    
    # API root
    path('', views.api_root, name='api-root'),
]

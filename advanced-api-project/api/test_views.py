from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from api.models import Book, Author

User = get_user_model()


class BookAPITestCase(APITestCase):
    """
    Test suite for the Book API endpoints.
    """
    
    def setUp(self):
        """Set up test data and client."""
        # Create test users
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='testpass123'
        )
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.R.R. Tolkien')
        self.author2 = Author.objects.create(name='George R.R. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='The Hobbit',
            publication_year=1937,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title='The Lord of the Rings',
            publication_year=1954,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title='A Game of Thrones',
            publication_year=1996,
            author=self.author2
        )
        
        # Set up the client
        self.client = APIClient()
    
    def test_list_books_unauthenticated(self):
        """Test that unauthenticated users can list books."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)
    
    def test_create_book_authenticated_admin(self):
        """Test that admin users can create books."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('book-create')
        data = {
            'title': 'The Silmarillion',
            'publication_year': 1977,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.latest('id').title, 'The Silmarillion')
    
    def test_create_book_authenticated_regular_user(self):
        """Test that regular users cannot create books."""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-create')
        data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_retrieve_book_detail(self):
        """Test retrieving a book's details."""
        url = reverse('book-detail', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
    
    def test_update_book_admin(self):
        """Test that admin users can update books."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('book-update', args=[self.book1.id])
        data = {'title': 'The Hobbit: Revised Edition'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit: Revised Edition')
    
    def test_delete_book_admin(self):
        """Test that admin users can delete books."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
    
    def test_filter_books_by_author(self):
        """Test filtering books by author."""
        url = f"{reverse('book-list')}?author={self.author1.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # 2 books by author1
        self.assertTrue(
            all(book['author'] == self.author1.id 
                for book in response.data['results'])
        )
    
    def test_search_books(self):
        """Test searching books by title and author name."""
        url = f"{reverse('book-list')}?search=Game"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'A Game of Thrones')
    
    def test_order_books(self):
        """Test ordering books by publication year."""
        url = f"{reverse('book-list')}?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data['results']]
        self.assertEqual(years, sorted(years, reverse=True))
    
    def test_create_book_invalid_year(self):
        """Test creating a book with an invalid publication year."""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('book-create')
        future_year = timezone.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author1.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
    
    def test_unauthorized_access(self):
        """Test that unauthorized users cannot modify books."""
        # Test unauthenticated user
        url = reverse('book-create')
        data = {'title': 'Unauthorized Book', 'publication_year': 2023, 'author': self.author1.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test regular user trying to update
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('book-update', args=[self.book1.id])
        response = self.client.patch(url, {'title': 'Updated Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test regular user trying to delete
        url = reverse('book-delete', args=[self.book1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

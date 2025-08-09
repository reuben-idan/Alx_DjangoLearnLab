# Advanced API Project

This project demonstrates the implementation of custom views and generic views in Django REST Framework (DRF) for building a book management API.

## Features

- **CRUD Operations**: Full support for creating, reading, updating, and deleting books and authors.
- **Custom Permissions**: Fine-grained access control with custom permission classes.
- **Filtering and Search**: Advanced filtering options for book listings.
- **Documentation**: Comprehensive API documentation with examples.

## API Endpoints

### Books

- **List/Create Books**
  - `GET /api/books/` - List all books
  - `POST /api/books/` - Create a new book (requires authentication)

- **Retrieve/Update/Delete Book**
  - `GET /api/books/<id>/` - Retrieve a specific book
  - `PUT /api/books/<id>/` - Update a book (requires authentication)
  - `PATCH /api/books/<id>/` - Partially update a book (requires authentication)
  - `DELETE /api/books/<id>/` - Delete a book (requires admin)

### Authors

- **List/Create Authors**
  - `GET /api/authors/` - List all authors
  - `POST /api/authors/` - Create a new author (requires authentication)

- **Retrieve/Update/Delete Author**
  - `GET /api/authors/<id>/` - Retrieve a specific author
  - `PUT /api/authors/<id>/` - Update an author (requires authentication)
  - `PATCH /api/authors/<id>/` - Partially update an author (requires authentication)
  - `DELETE /api/authors/<id>/` - Delete an author (requires admin)

## Query Parameters for Filtering Books

### Filtering
Filter books using exact matches on fields:
- `author` - Filter by exact author ID
- `publication_year` - Filter by exact publication year
- `publication_year__gt` - Filter by publication year greater than
- `publication_year__lt` - Filter by publication year less than

### Searching
Search across multiple fields using the `search` parameter:
- `search` - Case-insensitive search in title and author name
  Example: `?search=dune` will match books with "dune" in the title or author name

### Ordering
Order results using the `ordering` parameter:
- `ordering=field` - Order by field in ascending order
- `ordering=-field` - Order by field in descending order
- Multiple fields: `ordering=field1,-field2`

Supported fields: `title`, `publication_year`, `author__name`

### Examples
- `?author=1` - Get all books by author with ID 1
- `?publication_year__gt=2000` - Get books published after 2000
- `?search=sci-fi` - Search for "sci-fi" in title or author name
- `?ordering=-publication_year,title` - Order by year (newest first), then by title

## Authentication

All write operations (POST, PUT, PATCH, DELETE) require authentication. The API uses Django's built-in authentication system.

## Permissions

- **Read operations (GET)**: Available to all users
- **Write operations (POST, PUT, PATCH)**: Require authentication
- **Delete operations (DELETE)**: Require admin privileges

## Setup and Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Testing the API

You can test the API using tools like Postman, curl, or any HTTP client. Here are some example requests:

### List all books
```bash
curl http://localhost:8000/api/books/
```

### Create a new book
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Sample Book", "publication_year": 2023, "author": 1}'
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

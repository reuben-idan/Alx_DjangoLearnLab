# LibraryProject

This is a Django project created for learning and demonstration purposes. It includes a basic setup with the following structure:

- `manage.py`: Command-line utility to interact with the project.
- `settings.py`: Main configuration for the Django project.
- `urls.py`: URL declarations for the project.
- `wsgi.py` and `asgi.py`: Entry points for WSGI/ASGI-compatible web servers.
- `bookshelf/`: Django app containing the Book model and admin configuration.

To run the development server:

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the default Django welcome page.

For admin interface, visit http://127.0.0.1:8000/admin/ and use the superuser credentials.

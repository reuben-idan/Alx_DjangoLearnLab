# LibraryProject

This is the base Django project for the Introduction to Django learning lab. It was created using:

```bash
django-admin startproject LibraryProject
```

## Project Structure

- `manage.py`: Command-line utility to interact with this Django project.
- `LibraryProject/settings.py`: Main configuration for the Django project.
- `LibraryProject/urls.py`: URL declarations for the project.
- `LibraryProject/wsgi.py` and `asgi.py`: Entry points for WSGI/ASGI-compatible web servers.

## Running the Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ to see the default Django welcome page.

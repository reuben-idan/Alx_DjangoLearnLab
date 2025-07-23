# LibraryProject

This is a Django project created as part of the "Introduction to Django" learning lab. It demonstrates the default Django project structure and basic setup.

## Project Structure

- `manage.py`: Command-line utility to interact with this Django project.
- `LibraryProject/settings.py`: Main configuration for the Django project.
- `LibraryProject/urls.py`: URL declarations for the project.
- `LibraryProject/wsgi.py` and `asgi.py`: Entry points for WSGI/ASGI-compatible web servers.

## Running the Development Server

1. Open a terminal and navigate to this directory:
   ```bash
   cd Introduction_to_Django/LibraryProject
   ```
2. Start the development server:
   ```bash
   python manage.py runserver
   ```
3. Open your browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to view the default Django welcome page.

---

This project was created using:

```bash
django-admin startproject LibraryProject
```

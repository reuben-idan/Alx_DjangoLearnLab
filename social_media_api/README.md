# Social Media API - Initial Setup and Authentication

This project provides the initial setup for a Social Media API using Django and Django REST Framework with Token Authentication and a custom user model.

## Project Structure

- Project: `social_media_api/`
  - App: `accounts/` (custom user and auth endpoints)

## Requirements

- Python 3.12+
- Django 5.2+
- djangorestframework 3.16+
- Pillow (for image uploads)

Installed via:

```bash
pip install django djangorestframework pillow
```

## Initial Setup

From the project directory `social_media_api/`:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Admin superuser (optional):

```bash
python manage.py createsuperuser
```

## Custom User Model

Located at `accounts/models.py` as `User` extending `AbstractUser` with fields:

- `bio: TextField`
- `profile_picture: ImageField` (stored in `media/profiles/`)
- `followers: ManyToManyField('self', symmetrical=False)`

Set in `settings.py`:

- `AUTH_USER_MODEL = 'accounts.User'`
- `INSTALLED_APPS` includes `rest_framework`, `rest_framework.authtoken`, `accounts`
- Media: `MEDIA_URL = '/media/'`, `MEDIA_ROOT = BASE_DIR / 'media'`

## API Endpoints

Base path: `/api/accounts/`

- `POST /api/accounts/register/`
  - Body (JSON): `{ "username": "john", "email": "john@example.com", "password": "pass12345" }`
  - Response: `{ user: {...}, token: "<token>" }`

- `POST /api/accounts/login/`
  - Body (JSON): `{ "username": "john", "password": "pass12345" }`
  - Response: `{ user: {...}, token: "<token>" }`

- `GET /api/accounts/profile/`
  - Headers: `Authorization: Token <token>`
  - Response: user details

- `PUT/PATCH /api/accounts/profile/`
  - Headers: `Authorization: Token <token>`
  - For image upload, use multipart form data with `profile_picture` field.

## Quick cURL Examples

Register:

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com","password":"pass12345"}'
```

Login:

```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"pass12345"}'
```

Get profile:

```bash
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/accounts/profile/
```

Update profile (multipart with image):

```bash
curl -X PATCH http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Token <token>" \
  -F "first_name=John" \
  -F "bio=Hello world" \
  -F "profile_picture=@/full/path/to/file.jpg"
```

### Posts and Comments

Base path for posts/comments: `/api/`

- `GET /api/posts/` — list posts (paginated). Supports `?search=<term>` across title, content, author username.
- `POST /api/posts/` — create post. Body: `{ "title": "...", "content": "..." }`
- `GET /api/posts/{id}/` — retrieve post
- `PUT/PATCH /api/posts/{id}/` — update own post
- `DELETE /api/posts/{id}/` — delete own post

- `GET /api/comments/` — list comments (paginated)
- `POST /api/comments/` — create comment. Body: `{ "post": <post_id>, "content": "..." }`
- `GET /api/comments/{id}/` — retrieve comment
- `PUT/PATCH /api/comments/{id}/` — update own comment
- `DELETE /api/comments/{id}/` — delete own comment

All posts/comments endpoints require header: `Authorization: Token <token>`.

#### Quick cURL

Create post:

```bash
curl -X POST http://127.0.0.1:8000/api/posts/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","content":"World"}'
```

Search posts:

```bash
curl -H "Authorization: Token <token>" "http://127.0.0.1:8000/api/posts/?search=Hello"
```

Comment on a post:

```bash
curl -X POST http://127.0.0.1:8000/api/comments/ \
  -H "Authorization: Token <token>" \
  -H "Content-Type: application/json" \
  -d '{"post":1, "content":"Nice post!"}'
```

### Notes

- Default permission is `IsAuthenticated` in DRF settings; registration and login views override with `AllowAny`.
- Media files are served in development via `settings.DEBUG` and project `urls.py`.
- Admin shows custom `User` with extra fields.

## Next Steps

- Add endpoints to follow/unfollow users and list followers/following.
- Add posts app and content endpoints.
- Add pagination and throttling.

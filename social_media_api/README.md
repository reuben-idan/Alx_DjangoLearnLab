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

### Follows and Feed

Follow/unfollow other users and view a personalized feed of posts from users you follow.

Base paths:

- Accounts: `/api/accounts/`
- Feed: `/api/`

Endpoints:

- `POST /api/accounts/follow/<int:user_id>/` — follow a user
- `POST /api/accounts/unfollow/<int:user_id>/` — unfollow a user
- `GET /api/feed/` — list posts from followed users (paginated, newest first)

Headers: `Authorization: Token <token>` required.

Quick cURL:

```bash
# Follow user with ID 2
curl -X POST http://127.0.0.1:8000/api/accounts/follow/2/ \
  -H "Authorization: Token <token>"

# Unfollow user with ID 2
curl -X POST http://127.0.0.1:8000/api/accounts/unfollow/2/ \
  -H "Authorization: Token <token>"

# Get your feed
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/feed/
```

### Likes

Endpoints:

- `POST /api/posts/{id}/like/` — like a post (idempotent)
- `POST /api/posts/{id}/unlike/` — unlike a post

Headers: `Authorization: Token <token>` required.

Quick cURL:

```bash
# Like post 5
curl -X POST -H "Authorization: Token <token>" \
  http://127.0.0.1:8000/api/posts/5/like/

# Unlike post 5
curl -X POST -H "Authorization: Token <token>" \
  http://127.0.0.1:8000/api/posts/5/unlike/
```

### Notifications

Users receive notifications for:

- New followers
- Likes on their posts
- Comments on their posts

Endpoint:

- `GET /api/notifications/` — list notifications (unread first, then newest)

Quick cURL:

```bash
curl -H "Authorization: Token <token>" http://127.0.0.1:8000/api/notifications/
```

### Notes

- Default permission is `IsAuthenticated` in DRF settings; registration and login views override with `AllowAny`.
- Media files are served in development via `settings.DEBUG` and project `urls.py`.
- Admin shows custom `User` with extra fields.

## Next Steps

- Add endpoints to list a user's followers and following.
- Add throttling/rate limits for follow and like actions.
- Add OpenAPI/Swagger schema and automated tests.

## Deployment

This project is production-ready. Below are concise steps to deploy to Heroku (similar steps apply to Render/Railway/AWS).

### Production Settings

Key configuration is environment-driven in `social_media_api/social_media_api/settings.py`:

- `DJANGO_SECRET_KEY`: strong random string (required)
- `DJANGO_DEBUG`: `false` in production
- `DJANGO_ALLOWED_HOSTS`: comma-separated hostnames (e.g. `yourapp.herokuapp.com`)
- `DJANGO_CSRF_TRUSTED_ORIGINS`: comma-separated full origins (e.g. `https://yourapp.herokuapp.com`)
- `DJANGO_SECURE_SSL_REDIRECT`: `true`
- `DATABASE_URL`: Postgres URL (`postgres://USER:PASS@HOST:5432/DB`)

Static files are served via WhiteNoise. Run `collectstatic` during deploy.

### Requirements created

- `requirements.txt` includes: Django, djangorestframework, dj-database-url, WhiteNoise, Gunicorn, Pillow, psycopg2-binary
- `Procfile`: `web: gunicorn social_media_api.wsgi:application --log-file - --preload`
- `runtime.txt`: Python version
- `.env.example`: sample environment variables

### Deploy to Heroku

Prereqs: Heroku account and CLI installed, a Postgres add-on (Hobby Dev is fine).

```bash
# From the social_media_api directory
heroku create your-app-name
heroku buildpacks:set heroku/python
heroku addons:create heroku-postgresql:hobby-dev

# Config vars
heroku config:set DJANGO_SECRET_KEY="<strong-random>"
heroku config:set DJANGO_DEBUG=false
heroku config:set DJANGO_ALLOWED_HOSTS=your-app-name.herokuapp.com
heroku config:set DJANGO_CSRF_TRUSTED_ORIGINS=https://your-app-name.herokuapp.com

# Heroku provides DATABASE_URL automatically via add-on

# Push code
git push heroku main

# One-time setup
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput

# (optional) create superuser
heroku run python manage.py createsuperuser
```

Your API will be available at: `https://your-app-name.herokuapp.com/`

### Deploy to Render/Railway (outline)

- Create a Web Service from this repo.
- Environment: `PYTHON_VERSION=3.12.x`, set env vars as above.
- Start command: `gunicorn social_media_api.wsgi:application --log-file - --preload`
- Add managed Postgres; set `DATABASE_URL`.
- Add a post-deploy step to run `python manage.py migrate && python manage.py collectstatic --noinput`.

### Monitoring & Maintenance

- Logging: Review provider logs (Heroku `heroku logs --tail`).
- Errors: Consider Sentry for error monitoring.
- Security: Rotate `DJANGO_SECRET_KEY` if leaked; keep dependencies updated.
- Backups: Use managed DB automatic backups (Heroku PG Backups).


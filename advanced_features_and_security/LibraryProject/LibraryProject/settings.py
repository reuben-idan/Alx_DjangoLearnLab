AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Security Settings
DEBUG = False  # Disable DEBUG mode in production

SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking attacks
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-sniffing vulnerabilities
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is sent over HTTPS
SESSION_COOKIE_SECURE = True  # Ensure session cookie is sent over HTTPS
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS

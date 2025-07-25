AUTH_USER_MODEL = 'bookshelf.CustomUser'

# # Security Settings
# DEBUG = False  # Disable DEBUG mode in production

# SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
# X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking attacks
# SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-sniffing vulnerabilities
# CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is sent over HTTPS
# SESSION_COOKIE_SECURE = True  # Ensure session cookie is sent over HTTPS
# SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
# SECURE_HSTS_SECONDS with a value of 31536000
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# Secure Headers implementation
# AUTH_USER_MODEL = 'bookshelf.CustomUser'

# Security Settings
DEBUG = False  # Disable DEBUG mode in production

SECURE_SSL_REDIRECT = True  # Redirect all non-HTTPS requests to HTTPS
SECURE_HSTS_SECONDS = 31536000  # Instruct browsers to only access the site via HTTPS for one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Include all subdomains in the HSTS policy
SECURE_HSTS_PRELOAD = True  # Allow HSTS preloading

SECURE_BROWSER_XSS_FILTER = True  # Enable browser XSS filter
X_FRAME_OPTIONS = 'DENY'  # Prevent clickjacking attacks
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-sniffing vulnerabilities
CSRF_COOKIE_SECURE = True  # Ensure CSRF cookie is sent over HTTPS
SESSION_COOKIE_SECURE = True  # Ensure session cookie is sent over HTTPS
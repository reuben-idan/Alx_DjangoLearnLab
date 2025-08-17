# Authentication System Documentation

## Features

### 1. User Registration
- Email verification required for account activation
- Secure password validation
- Rate limiting on registration attempts

### 2. User Login/Logout
- Secure session management
- "Remember me" functionality
- Rate limiting on failed login attempts (5 attempts per minute)
- Session security with CSRF protection

### 3. Password Management
- Secure password change functionality
- Password reset via email
- Password strength validation

### 4. Profile Management
- Update user information
- Profile picture upload
- Email verification status

## Security Measures

### 1. Rate Limiting
- Login attempts: 5 per minute per IP/username
- Registration attempts: 3 per hour per IP
- Password reset: 3 per hour per email

### 2. CSRF Protection
- All forms include CSRF tokens
- Secure cookie settings
- Same-origin policy enforcement

### 3. Password Security
- Uses PBKDF2 with SHA-256 hashing
- Minimum password length: 8 characters
- Common password prevention
- Password history tracking

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Email Settings
Update `settings.py` with your email configuration:

```python
# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-email-password'
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser
```bash
python manage.py createsuperuser
```

## Testing

### Running Tests
```bash
python manage.py test blog.tests.test_auth
```

### Test Coverage
```bash
coverage run --source='.' manage.py test
coverage report
```

## API Endpoints

### Authentication
- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /signup/` - User registration
- `GET /verify-email/<uidb64>/<token>/` - Email verification

### Profile
- `GET /profile/` - View/Edit profile
- `POST /profile/` - Update profile
- `POST /password/change/` - Change password
- `POST /password/reset/` - Request password reset

## Troubleshooting

### Common Issues
1. **Email Not Sending**
   - Check email configuration in settings.py
   - Verify SMTP server credentials
   - Check spam folder

2. **Account Locked**
   - Wait for rate limit to expire (1 hour)
   - Contact support if issue persists

3. **Invalid Token**
   - Request new verification email
   - Ensure clicking link within 24 hours

## Security Best Practices

1. Always use HTTPS in production
2. Keep Django and dependencies updated
3. Use environment variables for sensitive data
4. Regularly backup user data
5. Monitor failed login attempts

## Support
For assistance, please contact support@yourdomain.com

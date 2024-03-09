# Initial Project Setup

This project uses Django and Allauth.

_NOTE: Commands were run within `poetry shell`._

```shell
poetry add django django-allaauth
django-admin startproject copilot
python manage.py startapp users
```

# OAuth2.0 using allauth Setup

To use OAuth2.0 with allauth, you need to add the following to the `INSTALLED_APPS` in `settings.py`:

```python
'django.contrib.sites',
'allauth',
'allauth.account',
'allauth.socialaccount',
'allauth.socialaccount.providers.github',
'allauth.socialaccount.providers.google',
```

Add the following to `MIDDLEWARE` in `settings.py`:
```python
    'allauth.account.middleware.AccountMiddleware',
```

Add the following configuration to the bottom of the `settings.py`:
```python
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

LOGIN_REDIRECT_URL = '/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

In your project's urls.py, include the allauth URLs:
```python
from django.urls import path, include  # Ensure include is imported here
...
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
]
```

Add the superuser:
```shell
python manage.py createsuperuser
```

To run the server:
```shell
python manage.py migrate
python manage.py runserver
```

Visit:
http://127.0.0.1:8000/admin/

Login with the superuser credentials.

# Social Application Setup

Add the social application for GitHub and Google.

## Google

Visit: https://console.cloud.google.com

Create a new project. APIs & Services -> API Library -> Enable the Google+ API for your project

Credentials -> "Create credentials" -> "OAuth client ID"
OAuth consent screen: Set up the application name, user support email, and adding any necessary scopes.
Application Type: "Web application" 
Under "Authorized redirect URIs," add the URI provided by Django AllAuth, typically:
- http://localhost:8000/accounts/google/login/callback/ for local development
- https://copilot.econtriver.com/accounts/google/login/callback/ for production
Once the OAuth client is created, you'll be provided with a Client ID and Client Secret. Keep these safe and confidential.
Scopes: For basic authentication and profile information, ensure the following scopes are added in the OAuth consent screen configuration:
- email
- profile
- openid

## GitHub

Visit: https://github.com/settings/apps (Settings -> Developer Settings)

Create New GitHub App
Homepage: https://copilot.econtriver.com
User authorization callback URLs:
- http://localhost:8000/accounts/github/login/callback/ for local development
- https://copilot.econtriver.com/accounts/github/login/callback/ for production

# Create the Templates

Create the following templates in the `templates` directory:

- `base.html`
- `account/login.html`
- `account/signup.html`

# To support email

Currently, the domain mail is handled by iCloud. An app-specific password is required to use the domain mail.

See: https://appleid.apple.com

Once you have the app-specific password, add the following to `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.me.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

Then in the `local_settings.py` file, add the following:

```python
DEFAULT_FROM_EMAIL = 'user@econtriver.com'
EMAIL_HOST_USER = 'user@me.com'
EMAIL_HOST_PASSWORD = 'app-specific-password'
```

## Test Emails

Enter the django shell:

```python
python manage.py shell
```

Then run the following:

```python
from django.core.mail import send_mail
send_mail('Test Subject', 'Test message.', 'from@example.com', ['to@example.com'], fail_silently=False)
```
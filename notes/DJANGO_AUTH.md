# Initial Project Setup

This project uses Django and Allauth.

_NOTE: Commands were run within `poetry shell`._

```shell
poetry add django django-allauth dj-rest-auth
django-admin startproject copilot
python manage.py startapp users
```

# OAuth2.0 using allauth Setup

To use OAuth2.0 with allauth, you need to add the following to the `INSTALLED_APPS` in `settings.py`:

```python
"django.contrib.sites",
"allauth",
"allauth.account",
"allauth.socialaccount",
"allauth.socialaccount.providers.github",
"allauth.socialaccount.providers.google",
```

Add the following to `MIDDLEWARE` in `settings.py`:

```python
"allauth.account.middleware.AccountMiddleware",
```

Add the following configuration to the bottom of the `settings.py`:

```python
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

SITE_ID = 1

LOGIN_REDIRECT_URL = "/"

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

In your project's urls.py, include the allauth URLs:

```python
from django.urls import path, include  # Ensure include is imported here

...
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
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

Visit: http://127.0.0.1:8000/admin/

Login with the superuser credentials.

# Social Application Setup

Add the social application for GitHub and Google.

## Google

Visit: https://console.cloud.google.com

Create a new project. APIs & Services -> API Library -> Enable the Google+ API for your project

Credentials -> "Create credentials" -> "OAuth client ID" OAuth consent screen: Set up the application name, user support
email, and adding any necessary scopes. Application Type: "Web application" Under "Authorized redirect URIs," add the
URI provided by Django AllAuth, typically:

- http://localhost:8000/accounts/google/login/callback/ for local development
- https://copilot.perpetuator.com/accounts/google/login/callback/ for production Once the OAuth client is created,
  you'll be provided with a Client ID and Client Secret. Keep these safe and confidential. Scopes: For basic
  authentication and profile information, ensure the following scopes are added in the OAuth consent screen
  configuration:
- email
- profile
- openid

From the admin site make sure to also 'choose' the sites for the social application:

- perpetuator.com
- 127.0.0.1:8000

## GitHub

Visit: https://github.com/settings/apps (Settings -> Developer Settings)

Create New GitHub App Homepage: https://copilot.perpetuator.com User authorization callback URLs:

- http://localhost:8000/accounts/github/login/callback/ for local development
- https://copilot.perpetuator.com/accounts/github/login/callback/ for production

GitHub & Google Production Request eula - https://copilot.perpetuator.com/eula/ privacy -
https://copilot.perpetuator.com/privacy/ status - https://copilot.perpetuator.com/status/ terms -
https://copilot.perpetuator.com/terms/

# Create the Templates

Create the following templates in the `templates` directory:

- `base.html`
- `account/login.html`
- `account/signup.html`

# To support email

Currently, the domain mail is handled by AWS SES. An app-specific username and password is created for the email
account. To generate these...

- Make sure the domain is set up correct in AWS SES, see [TERRAFORM](./TERRAFORM.md) for more information.

Then in the `.env` file, add the following:

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "email-smtp.us-east-1.amazonaws.com"  # Replace with your SES region
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "your-smtp-username"  # Replace with your SES SMTP username
EMAIL_HOST_PASSWORD = "your-smtp-password"  # Replace with your SES SMTP password
DEFAULT_FROM_EMAIL = "no-reply@yourdomain.com"  # Replace with your sender email

# Optional: Configuring email settings for allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
```

## Test Emails

Enter the django shell:

```shell
python manage.py shell
```

Then run the following:

```python
from django.core.mail import send_mail

send_mail(
    "Test Subject",
    "Test message.",
    "from@example.com",
    ["to@example.com"],
    fail_silently=False,
)
```

# Django REST API Token Authentication

Install Django REST Framework:

```shell
poetry add djangorestframework djangorestframework-simplejwt
```

Update Django settings to include the authentication classes:

```python
# settings.py

INSTALLED_APPS = [
    ...,
    "rest_framework",
    "rest_framework_simplejwt",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

In the `settings.py` file, add the following:

```python
from datetime import timedelta

SIMPLE_JWT = { 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5), 'REFRESH_TOKEN_LIFETIME': timedelta(days=1), ... } 
```

In the `urls.py` file, add the following:

```python
from django.urls import path
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )

urlpatterns = [ 
  ...,
  path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
  path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
  ...,
]
```

"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
import warnings
from unittest.mock import patch

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialLogin
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.test import Client, TestCase
from django.urls import reverse

from .adapters import MixedSocialAccountAdapter


def add_social_app(provider, name, site):
    app, created = SocialApp.objects.get_or_create(
        provider=provider, defaults={"name": name, "client_id": "test", "secret": "test"}
    )
    if created:
        app.sites.add(site)


def create_user(email):
    return User.objects.create_user(username=email, email=email)


class SocialAccountViewsTest(TestCase):
    def setUp(self):
        site = Site.objects.get(pk=1)
        add_social_app("google", "Google", site)
        add_social_app("github", "GitHub", site)

    def test_github_login_page_loads(self):
        url = reverse("github_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_google_login_page_loads(self):
        url = reverse("google_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class SocialAccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("testuser", "test@example.com", "testpassword")
        self.social_accounts_url = reverse("social_accounts")

    def test_social_accounts_login_required(self):
        response = self.client.get(self.social_accounts_url)
        self.assertEqual(response.status_code, 302)

    def test_social_accounts_success(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.social_accounts_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/social_accounts.html")


class AddSocialAccountTests(TestCase):
    def setUp(self):
        site = Site.objects.get(pk=1)
        add_social_app("google", "Google", site)
        self.client = Client()
        self.user = User.objects.create_user("testuser", "test@example.com", "testpassword")
        self.add_social_account_url = reverse("add_social_account", args=["google"])

    @patch("users.views.providers.registry.get_class")
    def test_add_social_account_success(self, mock_get_class):
        mock_provider_class = mock_get_class.return_value
        mock_provider_class.get_login_url.return_value = "/mock_auth_url"
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.add_social_account_url)
        self.assertRedirects(response, "/mock_auth_url", fetch_redirect_response=False)
        mock_provider_class.get_login_url.assert_called_once()
        mock_get_class.assert_called_once_with("google")

    @patch("users.views.providers.registry.get_class")
    def test_add_social_account_invalid_provider(self, mock_get_class):
        # Supress the logging of the 404 error: ......... 2024-04-10 15:38:20,132 WARNING django.request log_response
        # site-packages/django/utils/log.py:241 log Not Found: /accounts/social/add/google/
        logger = logging.getLogger("django.request")
        original_log_level = logger.getEffectiveLevel()
        logger.setLevel(logging.ERROR)
        try:
            warnings.filterwarnings("ignore", category=UserWarning)
            mock_get_class.return_value = None
            self.add_social_account_url = reverse("add_social_account", args=["google"])
            self.client.login(username="testuser", password="testpassword")
            response = self.client.get(self.add_social_account_url)
            self.assertEqual(response.status_code, 404)
        finally:
            # Restore the original logging level
            logger.setLevel(original_log_level)


class RemoveSocialAccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("testuser", "test@example.com", "testpassword")
        self.social_account = SocialAccount.objects.create(user=self.user, provider="TestProvider")
        self.remove_social_account_url = reverse("remove_social_account", args=[self.social_account.pk])

    def test_remove_social_account_success(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.remove_social_account_url)
        self.assertRedirects(response, reverse("social_accounts"))


class MixedSocialAccountAdapterTests(TestCase):
    def setUp(self):
        site = Site.objects.get(pk=1)
        add_social_app("google", "Google", site)

    def create_social_account(self, email, provider):
        user = create_user(email)
        social_account = SocialAccount.objects.create(user=user, provider=provider, uid=email)
        return social_account

    def test_pre_social_login_with_existing_user_and_social_account(self):
        email = "test@example.com"
        provider = "test_provider"
        social_account = self.create_social_account(email, provider)
        social_login = SocialLogin(user=social_account.user, account=social_account)

        adapter = MixedSocialAccountAdapter()
        adapter.pre_social_login(None, social_login)

        # Assert that no new social account is created
        self.assertEqual(SocialAccount.objects.filter(user=social_account.user, provider=provider).count(), 1)

    def test_pre_social_login_with_existing_user_no_social_account(self):
        email = "test@example.com"
        provider = "google"
        user = create_user(email)
        social_login = SocialLogin(user=user, account=SocialAccount(provider=provider, uid=email))

        adapter = MixedSocialAccountAdapter()
        adapter.pre_social_login(None, social_login)

        # Assert that a new social account is connected to the existing user
        self.assertTrue(SocialAccount.objects.filter(user=user, provider=provider).exists())

    def test_pre_social_login_with_no_existing_user(self):
        email = "test@example.com"
        provider = "test_provider"
        user = User(email=email, username=email)
        social_login = SocialLogin(user=user, account=SocialAccount(provider=provider, uid=email))

        adapter = MixedSocialAccountAdapter()
        adapter.pre_social_login(None, social_login)

        # Assert that no user is created in this step (user creation is handled elsewhere in the pipeline)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(email=email)

"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.test import TestCase
from django.urls import reverse


class AccountViewsTest(TestCase):

    def test_account_email_verification_sent_page_loads_successfully(self):
        url = reverse("account_email_verification_sent")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_account_confirm_email_page_loads(self):
        # This one is tricky because it requires a key
        # You'll need to create a user and trigger an email confirmation to test this properly
        pass

    def test_account_email_page_loads_successfully(self):
        url = reverse("account_email")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assuming login required

    def test_account_login_page_loads_successfully(self):
        url = reverse("account_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_account_logout_page_redirects_on_access(self):
        url = reverse("account_logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after logging out

    # Continue with other account-related views...


class HomePageAndUserViewsTest(TestCase):

    def test_home_page_loads_successfully(self):
        url = reverse("home_page")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_contact_page_loads_successfully(self):
        url = reverse("contact")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_landing_page_loads_successfully(self):
        url = reverse("landing_page")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_set_dark_mode_works(self):
        url = reverse("set_dark_mode")
        response = self.client.post(url, {"dark_mode": "true"})  # Assuming it requires a POST request with a parameter
        self.assertIn(
            response.status_code, [200, 302]
        )  # Depending on the implementation, it might redirect or return directly

    def test_user_preferences_js_loads_successfully(self):
        url = reverse("user_preferences_js")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class SocialAccountViewsTest(TestCase):
    def setUp(self):
        site = Site.objects.get(pk=1)
        SocialAccountViewsTest.add_social_app("google", "Google", site)
        SocialAccountViewsTest.add_social_app("github", "GitHub", site)

    @staticmethod
    def add_social_app(provider, name, site):
        app, created = SocialApp.objects.get_or_create(
            provider=provider, defaults={"name": name, "client_id": "test", "secret": "test"}
        )
        if created:
            app.sites.add(site)

    def test_github_login_page_loads(self):
        url = reverse("github_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)  # Or another appropriate status code

    def test_google_login_page_loads(self):
        url = reverse("google_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # And so on for other social account views...

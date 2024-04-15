"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import Client, TestCase
from django.urls import reverse

from users.models import UserPreferences


class HomePageAndUserViewsTest(TestCase):

    def test_home_page_loads_successfully(self):
        url = reverse("home_page")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_dashboard_page_loads_successfully(self):
        self.client = Client()
        self.user = User.objects.create_user("testuser", "test@example.com", "testpassword")
        self.client.login(username="testuser", password="testpassword")
        url = reverse("home_page")
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_landing_page_loads_successfully(self):
        url = reverse("landing_page")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_preferences_js_loads_successfully(self):
        url = reverse("user_preferences_js")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class SetDarkModeTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client = Client()
        self.client.login(username="testuser", password="12345")
        self.url = reverse("set_dark_mode")

    def test_post_request_sets_dark_mode_true(self):
        response = self.client.post(self.url, {"darkMode": "true"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        user_pref = UserPreferences.objects.get(user=self.user)
        self.assertTrue(user_pref.dark_mode)

    def test_post_request_sets_dark_mode_false(self):
        response = self.client.post(self.url, {"darkMode": "false"})
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True})
        user_pref = UserPreferences.objects.get(user=self.user)
        self.assertFalse(user_pref.dark_mode)

    def test_get_request_returns_failure(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": False})

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.post(self.url, {"darkMode": "true"})
        self.assertEqual(response.status_code, 302)


class ContactViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse("contact")

    def test_contact_view_get_request(self):
        response = self.client.get(self.contact_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "landing/contact.html")

    @patch("users.views.send_mail")
    def test_contact_form_submission_success(self, mock_send_mail):
        mock_send_mail.return_value = True
        form_data = {"name": "Test Name", "email": "test@example.com", "message": "Hello"}
        response = self.client.post(self.contact_url, form_data)
        self.assertRedirects(response, reverse("landing_page"))

    @patch("users.views.send_mail")
    def test_contact_form_submission_recently_submitted(self, mock_send_mail):
        mock_send_mail.return_value = True
        form_data = {"name": "Test Name", "email": "test@example.com", "message": "Hello"}
        self.client.post(self.contact_url, form_data)
        response = self.client.post(self.contact_url, form_data)
        messages = list(get_messages(response.wsgi_request))
        expected_message = "A contact us form was recently submitted."
        self.assertTrue(
            any(message.message == expected_message and message.level_tag == "warning" for message in messages),
            "Warning message about recent submission should be in messages",
        )
        self.assertRedirects(response, reverse("landing_page"))

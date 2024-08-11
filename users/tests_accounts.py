"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from django.test import TestCase
from django.urls import reverse


class AccountViewsTest(TestCase):

    def test_account_email_verification_sent_page_loads_successfully(self):
        url = reverse("account_email_verification_sent")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_account_confirm_email_page_loads(self):
        # TODO: Implement this test
        pass

    def test_account_email_page_loads_successfully(self):
        url = reverse("account_email")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_account_login_page_loads_successfully(self):
        url = reverse("account_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_account_logout_page_redirects_on_access(self):
        url = reverse("account_logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from django.test import TestCase
from django.urls import reverse


class AccountLoginPageTest(TestCase):

    def test_account_login_loads_successfully(self):
        url = reverse("account_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")

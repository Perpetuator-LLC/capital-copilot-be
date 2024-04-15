"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from unittest.mock import patch

from django.http import HttpResponseForbidden
from django.test import RequestFactory, TestCase

from .middleware import RestrictAdminMiddleware


class RestrictAdminMiddlewareTests(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RestrictAdminMiddleware(get_response=lambda request: None)

    def test_admin_access_with_allowed_ip(self):
        with patch("os.getenv", return_value="123.123.123.123"):
            request = self.factory.get("/admin/", REMOTE_ADDR="123.123.123.123")
            response = self.middleware(request)
            self.assertIsNone(response)

    def test_admin_access_with_disallowed_ip(self):
        with patch("os.getenv", return_value="123.123.123.123"):
            request = self.factory.get("/admin/", REMOTE_ADDR="111.111.111.111")
            response = self.middleware(request)
            self.assertIsInstance(response, HttpResponseForbidden)

    def test_admin_access_without_allowed_ips_set(self):
        with patch("os.getenv", return_value=None):
            request = self.factory.get("/admin/", REMOTE_ADDR="111.111.111.111")
            response = self.middleware(request)
            self.assertIsNone(response)

    def test_non_admin_access(self):
        with patch("os.getenv", return_value="123.123.123.123"):
            request = self.factory.get("/not-admin/", REMOTE_ADDR="111.111.111.111")
            response = self.middleware(request)
            self.assertIsNone(response)

"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from django.db import models


class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    ip_address = models.GenericIPAddressField()
    submission_time = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)


class UserPreferences(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="preferences")
    dark_mode = models.BooleanField(default=True)

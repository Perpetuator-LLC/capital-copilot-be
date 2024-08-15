"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from django.db import models


class UserPreferences(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE, related_name="preferences")
    dark_mode = models.BooleanField(default=True)

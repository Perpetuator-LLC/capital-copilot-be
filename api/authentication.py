"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class VerifiedEmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if not EmailAddress.objects.filter(user=user, email=user.email, verified=True).exists():
                raise Exception({"email": "Email address is not verified."})
                # raise serializers.ValidationError({"email": "Email address is not verified."})
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except Exception:
            raise

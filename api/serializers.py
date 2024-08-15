"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
from smtplib import SMTPException

from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from copilot import settings

# from rest_framework.response import Response

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# TODO: were using this to add user to token, but it has user ID and I think GQL will fail without existing user...
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         token["email"] = user.email  # Add custom claims, if user changes email, they get logged out of all sessions
#         return token
#
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#
#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)
#
#         return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )
        # optional_fields = ("first_name", "last_name",)

    def create(self, validated_data):
        try:
            with transaction.atomic():
                # Check if email already exists in EmailAddress
                if EmailAddress.objects.filter(email=validated_data["email"]).exists():
                    # TODO: Can we route these to the input field?
                    raise serializers.ValidationError({"email": "A user with that email already exists."})

                # Create the user
                user = User.objects.create(username=validated_data.get("username", ""), email=validated_data["email"])
                user.set_password(validated_data["password"])
                user.save()

                # Create the EmailAddress object
                email_address = EmailAddress.objects.create(
                    user=user,
                    email=validated_data["email"],
                    primary=True,
                    verified=False,
                )

                # Send verification email
                email_address.send_confirmation()
            return user
        except SMTPException as e:
            logging.exception("Failed to send verification email.", e)
            raise serializers.ValidationError({"email": "Failed to send verification email."})
        except ValidationError as e:
            logging.exception("Validation error:", e)
            raise e
        except Exception as e:
            logging.exception("Failed to create user.", e)
            error = "Failed to create user."
            if settings.DEBUG:
                error += str(e)
            raise serializers.ValidationError({"creation": error})

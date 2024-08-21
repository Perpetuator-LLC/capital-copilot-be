"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
from smtplib import SMTPException
from typing import Dict

from allauth.account.forms import ResetPasswordForm
from allauth.account.models import EmailAddress
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from copilot import settings


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs) -> Dict[str, str]:
        try:
            user = User.objects.get(username=attrs["username"])
            if user is None:
                user = User.objects.get(email=attrs["username"])  # See if username is email
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "User with this username or email does not exist."})
        if not EmailAddress.objects.filter(user=user, email=user.email, verified=True).exists():
            raise serializers.ValidationError(
                {"email": "Email is not verified. Please verify your email before logging in."}
            )
        data = super().validate(attrs)
        return data


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user is associated with this email address.")
        return value

    def save(self, request):
        # Trigger password reset using Allauth's ResetPasswordForm
        form = ResetPasswordForm({"email": self.validated_data["email"]})
        if form.is_valid():
            form.save(request=request)
        else:
            raise serializers.ValidationError(form.errors)


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
            logging.exception(f"Failed to send verification email: {str(e)}")
            raise serializers.ValidationError({"email": "Failed to send verification email."})
        except ValidationError as e:
            logging.exception(f"Validation error: {str(e)}")
            raise
        except Exception as e:
            logging.exception("Failed to create user.", e)
            error = "Failed to create user."
            if settings.DEBUG:
                error += str(e)
            raise serializers.ValidationError({"creation": error})

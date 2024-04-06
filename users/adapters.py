"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User


class MixedSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom social account adapter to handle social account connections and logins.
    """

    def pre_social_login(self, request, sociallogin):
        email = sociallogin.user.email
        if email:
            try:
                user = User.objects.get(email=email)
                existing_social_account = SocialAccount.objects.filter(user=user, provider=sociallogin.account.provider)
                if existing_social_account.exists():
                    # If the social account exists, we can potentially merge accounts or inform the user
                    pass
                else:
                    # If a user exists but doesn't have a social account for this provider, then connect the account
                    sociallogin.connect(request, user)
            except User.DoesNotExist:
                # No user with this email exists, so the pipeline will continue and eventually create a new user
                pass

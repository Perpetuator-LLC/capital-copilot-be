# ------------------------------------------------------------------------------
#  Copyright (c) 2024 eContriver LLC
#  This file is part of Capital Copilot from eContriver.
#  -
#  Capital Copilot from eContriver is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#  -
#  Capital Copilot from eContriver is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with Capital Copilot from eContriver.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

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

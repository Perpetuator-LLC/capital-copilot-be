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
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth.client import OAuthError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render


def landing_page(request):
    return render(request, "landing_page.html")


@login_required
def social_accounts(request):
    """View to list all linked social accounts for the current user"""
    accounts = SocialAccount.objects.filter(user=request.user)
    return render(request, "users/social_accounts.html", {"accounts": accounts})


@login_required
def add_social_account(request, provider_id):
    """Initiate the process of adding a new social account"""
    try:
        provider = providers.registry.get_class(provider_id)
        auth_url = provider.get_login_url(provider, request)
        return redirect(auth_url)
    except KeyError:
        return HttpResponse("Provider not found", status=404)
    except OAuthError as e:
        return HttpResponse(f"OAuth error: {e}", status=400)


@login_required
def remove_social_account(request, account_id):
    """Remove a linked social account"""
    account = SocialAccount.objects.get(pk=account_id, user=request.user)
    account.delete()
    return redirect("social_accounts")

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

import datetime
import os

from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.oauth.client import OAuthError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import ContactForm
from .models import ContactSubmission, UserPreferences


def landing_page(request):
    return render(request, "landing/home.html")


@login_required
def social_accounts(request):
    """View to list all linked social accounts for the current user"""
    user = request.user
    preferences = UserPreferences.objects.filter(user=user).first()
    accounts = SocialAccount.objects.filter(user=request.user)
    context = {
        "dark_mode": preferences.dark_mode if preferences else False,
        "accounts": accounts,
    }
    return render(request, "users/social_accounts.html", context=context)


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


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ip_address = get_client_ip(request)
            last_submission = (
                ContactSubmission.objects.filter(ip_address=ip_address).order_by("-submission_time").first()
            )
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            debounce_time = datetime.timedelta(minutes=5)
            if not last_submission or (timezone.now() - last_submission.submission_time > debounce_time):
                email_message = f"From: {name}\n\nEmail: {email}\n\n{message}"
                send_mail(
                    "Capital Copilot - Contact form submission",
                    email_message,
                    os.getenv("DEFAULT_FROM_EMAIL"),
                    [os.getenv("CONTACT_EMAIL")],
                    fail_silently=False,
                )
                ContactSubmission.objects.create(
                    name=name, email=email, message=message, ip_address=ip_address
                )  # Log this submission
                messages.success(request, "Your message has been sent successfully.")
                return redirect("landing_page")
            else:
                messages.warning(request, "A contact us form was recently submitted.")
                return redirect("landing_page")
    else:
        form = ContactForm()
    return render(request, "landing/contact.html", {"form": form})


def get_client_ip(request):
    """Get the client IP address from the request object."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@login_required
def set_dark_mode(request):
    if request.method == "POST":
        user_pref, created = UserPreferences.objects.get_or_create(user=request.user)
        user_pref.dark_mode = request.POST.get("darkMode") == "true"
        user_pref.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

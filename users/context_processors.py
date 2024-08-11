"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from django.urls import reverse
from django.utils.translation import gettext as _


def menu_items(request):
    items = [
        {"name": _("Home"), "link": reverse("home_page")},
        {"name": _("Contact"), "link": reverse("contact")},
    ]

    if request.user.is_staff:
        items.append({"name": _("Admin"), "link": reverse("admin:index")})

    return {"menu_items": items}


def account_menu_items(request):
    items = []
    if request.user.is_authenticated:
        items.append({"name": _("Change Email"), "link": reverse("account_email")})
        items.append({"name": _("Change Password"), "link": reverse("account_change_password")})
        items.append({"name": _("Logout"), "link": reverse("account_logout")})
        items.append({"name": _("Social Accounts"), "link": reverse("social_accounts")})
    else:
        items.append({"name": _("Sign Up"), "link": reverse("account_signup")})
        items.append({"name": _("Login"), "link": reverse("account_login")})

    return {"account_menu_items": items}


def footer_items(request):
    items = [
        {"name": _("Home"), "link": reverse("home_page")},
        {"name": _("Contact"), "link": reverse("contact")},
        {"name": "Discord", "link": "https://discord.gg/RqFW3468wY"},
    ]

    if request.user.is_authenticated:
        items.append({"name": _("Commercial"), "link": reverse("landing_page")})

    if request.user.is_staff:
        items.append({"name": _("Admin"), "link": reverse("admin:index")})

    return {"footer_items": items}


def dark_mode_context(request):
    """
    This context processor adds a user's dark mode preference to the context, so we can use it in templates. This is
    only needed so that dark and light modes don't flash on load. By setting the color scheme in the HTML, we can
    avoid this.
    :param request: The request object.
    :return: A dictionary with the user's dark mode preference.
    """
    user_prefers_dark_mode = True

    if hasattr(request.user, "preferences") and hasattr(request.user.preferences, "dark_mode"):
        user_prefers_dark_mode = request.user.preferences.dark_mode

    return {
        "user_prefers_dark_mode": user_prefers_dark_mode,
    }

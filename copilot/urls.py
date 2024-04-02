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

"""
URL configuration for copilot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from copilot_plugin_dashboard import views as dashboard_views
from copilot_plugin_view import views as view_views
from django.contrib import admin
from django.urls import include, path

from users import views

urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("landing/", views.landing_page, name="landing_page"),
    path("dashboard/", dashboard_views.dashboard_page, name="dashboard_page"),
    path("view/", view_views.dashboard_page, name="view_page"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/social/", views.social_accounts, name="social_accounts"),
    path(
        "accounts/social/add/<provider_id>/",
        views.add_social_account,
        name="add_social_account",
    ),
    path(
        "accounts/social/remove/<int:account_id>/",
        views.remove_social_account,
        name="remove_social_account",
    ),
    path("contact/", views.contact, name="contact"),
    path("set_dark_mode/", views.set_dark_mode, name="set_dark_mode"),
    path("users/preferences.js", views.user_preferences_js, name="user_preferences_js"),
]

"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from django.urls import path
from django.utils.functional import SimpleLazyObject
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user(request):
    jwt_auth = JWTAuthentication()
    result = jwt_auth.authenticate(request)
    if result:
        return result[0]  # Return only the user

    return None


class CustomGraphQLView(GraphQLView):
    def get_context(self, request):
        # Ensure the user is lazy-loaded, only processed when accessed
        request.user = SimpleLazyObject(lambda: get_user(request))
        return request


urlpatterns = [
    path("", csrf_exempt(CustomGraphQLView.as_view(graphiql=True)), name="graphql"),
]

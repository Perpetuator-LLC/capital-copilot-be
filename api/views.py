"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CustomTokenObtainPairSerializer,
    PasswordResetSerializer,
    RegisterSerializer,
)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer  # type: ignore[assignment] # reason: TokenViewBase is None


class PasswordResetView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request=request)
        return Response({"detail": "Password reset e-mail has been sent."}, status=status.HTTP_200_OK)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # NOTE: The front-end should handle the error messages in this raised exception format...
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "detail": f"Welcome {user.username}! Verify Email to activate account.",
            },
            status=status.HTTP_201_CREATED,
        )


# class SocialLoginView(views.APIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request, provider):
#         token = request.data.get("access_token")
#         adapter_class = {
#             "google": GoogleOAuth2Adapter,
#             "github": GitHubOAuth2Adapter,
#         }.get(provider)
#
#         if adapter_class is None:
#             return Response({"error": "Unsupported provider"}, status=status.HTTP_400_BAD_REQUEST)
#
#         adapter = adapter_class()
#         app = adapter.get_provider().get_app(request)
#         token = adapter.parse_token({"access_token": token})
#         social_login = adapter.complete_login(request, app, token, response={"access_token": token})
#
#         try:
#             complete_social_login(request, social_login)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#         user = social_login.user
#         if not user.is_active:
#             return Response({"error": "User inactive or deleted"}, status=status.HTTP_400_BAD_REQUEST)
#
#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {
#                 "refresh": str(refresh),
#                 "access": str(refresh.access_token),
#             },
#             status=status.HTTP_200_OK,
#         )

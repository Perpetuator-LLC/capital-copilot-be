"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

# Thought this was neededd, but it turns out the JWT has the User ID and APIs should not work if not validated...
# from django.http import JsonResponse
# from django.utils.deprecation import MiddlewareMixin
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.contrib.auth.models import User
#
#
# class ValidateUserMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.path in ["/api/register/", "/api/login/"]:
#             return None
#         authentication = JWTAuthentication()
#         try:
#             response = authentication.authenticate(request)
#             if response is not None:
#                 user, token = response
#                 # Check if the user from the token matches a valid user in the database
#                 if not User.objects.filter(email=token['email'], is_active=True).exists():
#                     return JsonResponse({'detail': 'User does not exist or is not active'}, status=401)
#         except Exception as e:
#             return JsonResponse({'detail': str(e)}, status=401)

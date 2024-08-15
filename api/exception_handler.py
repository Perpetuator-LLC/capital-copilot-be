"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

# from rest_framework.views import exception_handler
# from rest_framework.exceptions import ValidationError
#
# def api_exception_handler(exc, context):
#     # Call DRF's default exception handler to get the standard error response.
#     response = exception_handler(exc, context)
#
#     # If the exception is a validation error, modify the response.
#     if isinstance(exc, ValidationError) and response is not None:
#         response.data = {
#             "errors": response.data  # Move the original error details under "errors" field
#         }
#
#     return response

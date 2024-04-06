"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import os

from django.http import HttpResponseForbidden


def is_valid_ip(ip_addr, allowed_ips):
    # Consider supporting ranges, subnets, etc. (see package: `ipaddress`)
    return ip_addr in allowed_ips


class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/"):
            allowed_ips = os.getenv("ADMIN_ALLOWED_IPS").split(",") if os.getenv("ADMIN_ALLOWED_IPS") else []
            num_ips = len(allowed_ips)
            if num_ips > 0:
                ip_addr = request.META.get("REMOTE_ADDR")
                if not is_valid_ip(ip_addr, allowed_ips):
                    return HttpResponseForbidden("Access Denied")
                    # return HttpResponseForbidden(
                    #     f"Access Denied - Allowed: {allowed_ips} ({num_ips}) - Current: {ip_addr}"
                    # )

        response = self.get_response(request)
        return response

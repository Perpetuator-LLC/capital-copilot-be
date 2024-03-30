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
                    # return HttpResponseForbidden(f"Access Denied")
                    return HttpResponseForbidden(
                        f"Access Denied - Allowed: {allowed_ips} ({num_ips}) - Current: {ip_addr}"
                    )

        response = self.get_response(request)
        return response

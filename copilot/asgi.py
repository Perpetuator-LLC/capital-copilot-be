"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "copilot.settings")

application = get_asgi_application()

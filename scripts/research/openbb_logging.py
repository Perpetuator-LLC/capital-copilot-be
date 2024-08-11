"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging

from openbb import obb  # noqa: F401

from copilot.copilot_shared import process_env
from copilot.logging_service import LoggingService

if __name__ == "__main__":
    process_env()
    LoggingService.configure_logging({"stdout": logging.DEBUG})
    logging.debug("does it print?")

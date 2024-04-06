"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
import sys

from copilot.copilot_shared import process_env
from copilot.logging_service import LoggingService

if __name__ == "__main__":
    try:
        process_env()
        LoggingService.configure_logging(logging.DEBUG)
        logging.debug("test.py: main() started")
    except Exception as e:
        logging.error(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)

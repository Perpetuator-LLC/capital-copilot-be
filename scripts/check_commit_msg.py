"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
import re
import sys

from copilot.copilot_shared import process_env
from copilot.logging_service import LoggingService


def check_message(semantic_pattern, message):
    if not re.match(semantic_pattern, message):
        logging.error("Commit message doesn't follow Semantic Commit Messages format")
        return 1
    return 0


def main():
    process_env()
    LoggingService.configure_logging()
    logging.debug(f"Received commit message file: {sys.argv[1]}")
    with open(sys.argv[1], "r") as f:
        commit_message = f.read().strip()
    logging.debug(f"Commit message: '{commit_message}'")
    semantic_pattern = r"^(feat|fix|docs|style|refactor|perf|test|chore)(?:\(.*\))?: .+"
    sys.exit(check_message(semantic_pattern, commit_message))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)

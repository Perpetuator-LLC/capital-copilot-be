"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
import os
import re
import sys
from datetime import datetime

from copilot.copilot_shared import process_env


def main():
    process_env()
    logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "INFO"))
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.realpath(os.path.join(script_dir, ".."))
    files = sys.argv[1:] if len(sys.argv) > 1 else [repo_dir]

    failed = False

    for file in files:
        check_file = file if os.path.isfile(file) else os.path.realpath(os.path.join(repo_dir, file))
        if not check_header(check_file):
            checked_file = file if os.path.samefile(check_file, file) else (f"{file} (also checked {check_file}")
            logging.error(f"Copyright header check failed for {checked_file}")
            failed = True

    if failed:
        sys.exit(1)
    logging.debug(f"Copyright header check passed for {files}")


def check_header(filename):
    logging.debug(f"Checking file {filename}")
    with open(filename, "r") as file:
        content = file.read()
        pattern = expected_copyright()
        return bool(pattern.search(content))


def expected_copyright():
    pattern = re.compile(r"Copyright \(c\) .*" + str(datetime.now().year) + r" Perpetuator LLC")
    return pattern


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.exception(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)

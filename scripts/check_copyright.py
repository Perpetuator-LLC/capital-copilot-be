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

import logging
import os
import re
import sys
from datetime import datetime

from copilot.copilot_shared import configure_logging, process_env


def main():
    process_env()
    configure_logging()
    script_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.realpath(os.path.join(script_dir, ".."))
    files = sys.argv[1:] if len(sys.argv) > 1 else [repo_dir]

    failed = False

    for file in files:
        check_file = file if os.path.isfile(file) else os.path.realpath(os.path.join(repo_dir, file))
        if not check_header(check_file):
            checked_file = file if os.path.samefile(check_file, file) else (f"{file} (also checked {check_file}")
            logging.error(f"GPL header check failed for {checked_file}")
            failed = True

    if failed:
        sys.exit(1)
    logging.debug(f"GPL header check passed for {files}")


def check_header(filename):
    logging.debug(f"Checking file {filename}")
    with open(filename, "r") as file:
        content = file.read()
        pattern = expected_copyright()
        return bool(pattern.search(content))


def expected_copyright():
    pattern = re.compile(r"Copyright \(c\) .*" + str(datetime.now().year) + r" eContriver LLC")
    return pattern


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)

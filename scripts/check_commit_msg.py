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
import re
import sys

from copilot.copilot_shared import configure_logging, process_env


def check_message(semantic_pattern, message):
    if not re.match(semantic_pattern, message):
        logging.error("Commit message doesn't follow Semantic Commit Messages format")
        return 1
    return 0


def main():
    process_env()
    configure_logging()
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

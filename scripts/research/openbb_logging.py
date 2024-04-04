# ------------------------------------------------------------------------------
# Copyright (c) 2024 eContriver LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# ------------------------------------------------------------------------------

import logging

from openbb import obb  # noqa: F401

from copilot.copilot_shared import process_env
from copilot.logging_service import LoggingService

if __name__ == "__main__":
    process_env()
    LoggingService.configure_logging({"stdout": logging.DEBUG})
    logging.debug("does it print?")

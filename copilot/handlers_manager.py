# ------------------------------------------------------------------------------
# Portions of this file are derived from OpenBB, Copyright (c) 2021-2023 OpenBB Inc.
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
import sys
from typing import Dict, List

from copilot.formatter_with_exceptions import FormatterWithExceptions
from copilot.path_tracking_file_handler import PathTrackingFileHandler


class HandlersManager:
    _handlers: List[str]

    def __init__(self, handlers: List[str], levels: Dict, logs_dir: str | None = None):
        self._handlers = handlers

        for handler_type in self._handlers:
            level = levels.get(handler_type, logging.INFO)
            if handler_type == "stdout":
                self._add_stdout_handler(level)
            elif handler_type == "noop":
                self._add_noop_handler(level)
            elif handler_type == "file":
                self._add_file_handler(level, logs_dir)
            else:  # this is where we can add posthog
                logging.getLogger().debug("Unknown log handler.")

    @staticmethod
    def _add_stdout_handler(level):
        handler = logging.StreamHandler(sys.stdout)
        formatter = FormatterWithExceptions()
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logging.getLogger().addHandler(handler)

    @staticmethod
    def _add_noop_handler(level):
        handler = logging.NullHandler()
        formatter = FormatterWithExceptions()
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logging.getLogger().addHandler(handler)

    @staticmethod
    def _add_file_handler(level, logs_dir: str | None = None):
        handler = PathTrackingFileHandler(logs_dir)
        formatter = FormatterWithExceptions()
        handler.setFormatter(formatter)
        handler.setLevel(level)
        logging.getLogger().addHandler(handler)

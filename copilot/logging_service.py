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

import json
import logging
import os

from copilot.formatter_with_exceptions import FormatterWithExceptions
from copilot.handlers_manager import HandlersManager


class LoggingService:
    @staticmethod
    def configure_logging(levels=None, output_dir: str | None = None) -> None:
        if levels is None:
            levels = {}
        logger = logging.getLogger()
        default_levels = {
            "file": logging.DEBUG,
            "stdout": LoggingService.get_log_level(),
        }
        levels = {**default_levels, **levels}
        # logger.setLevel(logging.DEBUG)
        logging.basicConfig(
            level=logging.DEBUG,  # Required for debug messages to be written to the file
            format=FormatterWithExceptions.LOGFORMAT,
            datefmt=FormatterWithExceptions.DATEFORMAT,
            handlers=[],  # Remove the default handler, note this will also remove OpenBB logging
            force=True,
        )
        HandlersManager(["file", "stdout"], levels, output_dir)

        # Configure STDOUT (INFO unless LOG_LEVEL or level is set)
        # out_handler = logging.StreamHandler(sys.stdout)
        # out_handler.setLevel(level)
        # out_handler.setFormatter(logging.Formatter("%(message)s"))
        # logging.getLogger().addHandler(out_handler)

        # Configure file logging (DEBUG with timestamps etc.)
        # if not output_dir:
        #     script_dir = os.path.dirname(os.path.realpath(__file__))
        #     repo_dir = os.path.realpath(os.path.join(script_dir, ".."))
        #     output_dir = os.path.join(repo_dir, "logs")
        # if not os.path.exists(output_dir):
        #     os.makedirs(output_dir)
        # # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        # # run_log = os.path.join(output_dir, f'run.{timestamp}.log')
        # run_log = os.path.join(output_dir, f'run.log')
        # file_handler = logging.FileHandler(run_log, mode="w")
        # file_handler.setLevel(logging.DEBUG)
        # file_handler.setFormatter(logging.Formatter(LoggingService.LOGFORMAT, datefmt=LoggingService.DATEFORMAT))
        # logging.getLogger().addHandler(file_handler)

        # LOGPREFIXFORMAT = (
        #     "%(levelname)s|%(appName)s|%(commitHash)s|%(appId)s|%(sessionId)s|%(userId)s|"
        # )

        file_logging = False
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                file_logging = True
                logging.info(f"Logging to {LoggingService.file_link_format(handler.baseFilename)}")
        if not file_logging:
            logging.info("Logging to stdout")
        logging.debug("Logging set to %s", logging.getLogger().handlers)
        logger.debug(
            "LOGFORMAT: %s%s",
            FormatterWithExceptions.LOGPREFIXFORMAT.replace("|", "-"),
            FormatterWithExceptions.LOGFORMAT.replace("|", "-"),
        )

    @staticmethod
    def file_link_format(profile_log: str) -> str:
        # This syntax was not working with the default run console until [X] Run with Python Console was checked
        return "file://{}".format(str(profile_log))
        # The following only works if the file already exists... which most of the time the log isn't created until
        # after the process is nearly complete so this won't work
        # return f"""File "{profile_log}", line 1, in log"""

    @staticmethod
    def dump_object(obj):
        def default_serializer(o):
            if hasattr(o, "__dict__"):
                return o.__dict__
            else:
                return str(o)

        return json.dumps(obj, default=default_serializer, indent=2)

    @staticmethod
    def print_pkg_versions():
        from importlib.metadata import distributions

        for dist in distributions():
            print(f"{dist.metadata['Name']} {dist.version}")
        # import pkg_resources
        # for dist in pkg_resources.working_set:
        #     print(f"{dist.project_name} {dist.version}")

    @staticmethod
    def get_log_level():
        log_level_mapping = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
        log_level = log_level_mapping.get(log_level_str, logging.INFO)
        return log_level

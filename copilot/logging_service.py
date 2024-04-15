# """
# Portions of this file are derived from OpenBB, Copyright (c) 2021-2023 OpenBB Inc.
# Copyright (c) 2024 eContriver LLC
#
# This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
# See the LICENSE file in the root of this project for the full license text.
# """
#
# import logging
# import os
# import json
#
# from copilot.formatter_with_exceptions import FormatterWithExceptions
# from copilot.handlers_manager import HandlersManager
#
#
# class LoggingService:
#     LOGGING_CONFIGURED = False
#
#     @staticmethod
#     def configure_logging(levels=None, output_dir: str | None = None) -> None:
#         if levels is None:
#             levels = {}
#         default_levels = {
#             "file": logging.DEBUG,
#             "stdout": LoggingService.get_log_level(),
#         }
#         levels = {**default_levels, **levels}
#         if output_dir and not os.path.exists(output_dir):
#             os.makedirs(output_dir)
#         handlers = ["file", "stdout"] if output_dir else ["stdout"]
#         HandlersManager(handlers, levels, output_dir)
#
#         logger = logging.getLogger()
#         logger.setLevel(logging.DEBUG)  # Lowest level to capture everything
#
#         # Clear existing handlers to avoid duplicate logging
#         logger.handlers = []
#
#         log_format = FormatterWithExceptions.LOGFORMAT
#         date_format = FormatterWithExceptions.DATEFORMAT
#
#         # Setup file handler if specified
#         if output_dir:
#             log_file = os.path.join(output_dir, "copilot.log")
#             file_handler = logging.FileHandler(log_file)
#             file_handler.setLevel(levels['file'])
#             file_handler.setFormatter(logging.Formatter(log_format, date_format))
#             logger.addHandler(file_handler)
#             if levels['file'] <= logging.DEBUG:
#                 LoggingService.print_pkg_versions(logger)  # Print package versions to log file if in DEBUG
#
#         # Setup stdout handler
#         stdout_handler = logging.StreamHandler()
#         stdout_handler.setLevel(levels['stdout'])
#         stdout_handler.setFormatter(logging.Formatter(log_format, date_format))
#         logger.addHandler(stdout_handler)
#
#         logger.debug(f"Logging to {LoggingService.file_link_format(log_file)}")
#         LoggingService.LOGGING_CONFIGURED = True
#
#     @staticmethod
#     def file_link_format(profile_log: str) -> str:
#         # This syntax was not working with the default run console until [X] Run with Python Console was checked
#         return f"file://{profile_log}"
#         # The following only works if the file already exists... which most of the time the log isn't created until
#         # after the process is nearly complete so this won't work
#         # return f"""File "{profile_log}", line 1, in log"""
#
#     @staticmethod
#     def dump_object(obj):
#         def default_serializer(o):
#             if hasattr(o, "__dict__"):
#                 return o.__dict__
#             else:
#                 return str(o)
#
#         return json.dumps(obj, default=default_serializer, indent=2)
#
#     @staticmethod
#     def print_pkg_versions(logger: logging.Logger):
#         from importlib.metadata import distributions
#         logger.debug("Package Versions:")
#         for dist in distributions():
#             logger.debug(f"{dist.metadata['Name']} {dist.version}")
#         # import pkg_resources
#         # for dist in pkg_resources.working_set:
#         #     print(f"{dist.project_name} {dist.version}")
#
#     @staticmethod
#     def get_log_level():
#         log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
#         level = logging.getLevelName(log_level_str)
#         return logging.INFO if type(level) is str else level
#         # log_level_mapping = {
#         #     "DEBUG": logging.DEBUG,
#         #     "INFO": logging.INFO,
#         #     "WARNING": logging.WARNING,
#         #     "ERROR": logging.ERROR,
#         #     "CRITICAL": logging.CRITICAL,
#         # }
#         # return log_level_mapping.get(log_level_str, logging.INFO)

# """
# Portions of this file are derived from OpenBB, Copyright (c) 2021-2023 OpenBB Inc.
# Copyright (c) 2024 eContriver LLC
#
# This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
# See the LICENSE file in the root of this project for the full license text.
# """
#
# import os
# from logging.handlers import TimedRotatingFileHandler
# from pathlib import Path
#
# from copilot.expired_files import (
#     get_expired_file_list,
#     get_timestamp_from_x_days,
#     remove_file_list,
# )
#
# ARCHIVES_FOLDER_NAME = "archives"
# TMP_FOLDER_NAME = "tmp"
#
#
# class PathTrackingFileHandler(TimedRotatingFileHandler):
#     logs_directory: Path
#
#     @staticmethod
#     def build_log_file_path(logs_dir: Path) -> Path:
#         # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
#         # path = logs_dir.joinpath(f"run.{timestamp}.log")
#         path = logs_dir.joinpath("copilot")
#         return Path(path)
#
#     def clean_expired_files(self, before_timestamp: float):
#         """Remove expired files from logs directory"""
#
#         logs_dir = self.logs_directory
#         archives_directory = logs_dir / ARCHIVES_FOLDER_NAME
#         tmp_directory = logs_dir / TMP_FOLDER_NAME
#
#         expired_logs_file_list = get_expired_file_list(
#             directory=logs_dir,
#             before_timestamp=before_timestamp,
#         )
#         expired_archives_file_list = get_expired_file_list(
#             directory=archives_directory,
#             before_timestamp=before_timestamp,
#         )
#         expired_tmp_file_list = get_expired_file_list(
#             directory=tmp_directory,
#             before_timestamp=before_timestamp,
#         )
#         remove_file_list(file_list=expired_logs_file_list)
#         remove_file_list(file_list=expired_archives_file_list)
#         remove_file_list(file_list=expired_tmp_file_list)
#
#     def __init__(
#         self,
#         logs_dir,
#         *args,
#         **kwargs,
#     ) -> None:
#         if logs_dir:
#             self.logs_directory = Path(logs_dir).absolute()
#         else:
#             script_dir = os.path.dirname(os.path.realpath(__file__))
#             repo_dir = os.path.realpath(os.path.join(script_dir, ".."))
#             self.logs_directory = Path(os.path.join(repo_dir, "logs")).absolute()
#         filename = str(self.build_log_file_path(self.logs_directory))
#         role_over_frequency = "M"
#         kwargs["when"] = role_over_frequency
#
#         super().__init__(filename, *args, **kwargs)
#
#         self.suffix += ".log"
#
#         self.clean_expired_files(before_timestamp=get_timestamp_from_x_days(x=5))

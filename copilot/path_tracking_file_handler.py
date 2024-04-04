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


import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from copilot.expired_files import (
    get_expired_file_list,
    get_timestamp_from_x_days,
    remove_file_list,
)

ARCHIVES_FOLDER_NAME = "archives"
TMP_FOLDER_NAME = "tmp"


class PathTrackingFileHandler(TimedRotatingFileHandler):
    logs_directory: Path

    @staticmethod
    def build_log_file_path(logs_dir: Path) -> Path:
        # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        # path = logs_dir.joinpath(f"run.{timestamp}.log")
        path = logs_dir.joinpath("run")
        return Path(path)

    def clean_expired_files(self, before_timestamp: float):
        """Remove expired files from logs directory"""

        logs_dir = self.logs_directory
        archives_directory = logs_dir / ARCHIVES_FOLDER_NAME
        tmp_directory = logs_dir / TMP_FOLDER_NAME

        expired_logs_file_list = get_expired_file_list(
            directory=logs_dir,
            before_timestamp=before_timestamp,
        )
        expired_archives_file_list = get_expired_file_list(
            directory=archives_directory,
            before_timestamp=before_timestamp,
        )
        expired_tmp_file_list = get_expired_file_list(
            directory=tmp_directory,
            before_timestamp=before_timestamp,
        )
        remove_file_list(file_list=expired_logs_file_list)
        remove_file_list(file_list=expired_archives_file_list)
        remove_file_list(file_list=expired_tmp_file_list)

    # OVERRIDE
    def __init__(
        self,
        logs_dir,
        *args,
        **kwargs,
    ) -> None:
        if logs_dir:
            self.logs_directory = Path(logs_dir).absolute()
        else:
            script_dir = os.path.dirname(os.path.realpath(__file__))
            repo_dir = os.path.realpath(os.path.join(script_dir, ".."))
            self.logs_directory = Path(os.path.join(repo_dir, "logs")).absolute()
        filename = str(self.build_log_file_path(self.logs_directory))
        role_over_frequency = "M"
        kwargs["when"] = role_over_frequency

        super().__init__(filename, *args, **kwargs)

        self.suffix += ".log"

        self.clean_expired_files(before_timestamp=get_timestamp_from_x_days(x=5))

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


import contextlib
from datetime import datetime
from pathlib import Path
from typing import List

# IMPORTATION THIRDPARTY

# IMPORTATION INTERNAL


def get_timestamp_from_x_days(x: int) -> float:
    timestamp_from_x_days = datetime.now().timestamp() - x * 86400
    return timestamp_from_x_days


def get_expired_file_list(directory: Path, before_timestamp: float) -> List[Path]:
    expired_files = []
    if directory.is_dir():  # Check if the directory exists and is a directory
        for file in directory.iterdir():
            if file.is_file() and file.lstat().st_mtime < before_timestamp:
                expired_files.append(file)

    return expired_files


def remove_file_list(file_list: List[Path]):
    for file in file_list:
        with contextlib.suppress(PermissionError):
            file.unlink(missing_ok=True)

"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import os

from dotenv import load_dotenv


def process_env():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.realpath(os.path.join(script_dir, ".."))
    dotenv_file = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_file)
    return dotenv_file

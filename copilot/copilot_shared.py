"""
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import os

from dotenv import load_dotenv

# def get_collection():
#     collection = "test-collection"
#     return collection


def process_env():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.realpath(os.path.join(script_dir, ".."))
    dotenv_file = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_file)
    return dotenv_file

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

import json
import logging
import os

from dotenv import load_dotenv


def configure_logging(level=None):
    level = level if level else get_log_level()
    logger = logging.getLogger()
    logger.setLevel(level)
    logging.basicConfig(level=level)


def dump_object(obj):
    def default_serializer(o):
        if hasattr(o, "__dict__"):
            return o.__dict__
        else:
            return str(o)

    return json.dumps(obj, default=default_serializer, indent=2)


def print_pkg_versions():
    from importlib.metadata import distributions

    for dist in distributions():
        print(f"{dist.metadata['Name']} {dist.version}")
    # import pkg_resources
    # for dist in pkg_resources.working_set:
    #     print(f"{dist.project_name} {dist.version}")


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


def get_collection():
    collection = "test-collection"
    return collection


def process_env():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    base_dir = os.path.realpath(os.path.join(script_dir, ".."))
    dotenv_file = os.path.join(base_dir, ".env")
    load_dotenv(dotenv_file)
    return dotenv_file

# Copyright (c) 2024 Perpetuator LLC
import json
import logging
import os
import sys

import dotenv

# Shall only use python builtins/standard packages here


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
    if os.getenv("DEBUG") == "1":  # NOTE: this is legacy, use LOG_LEVEL instead
        return logging.DEBUG
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


def process_env(script_dir, env=None):
    envs = ["prod", "stage"]
    env = env if env or len(sys.argv) <= 1 else sys.argv[1]
    if env not in envs:
        raise ValueError(
            f"Incorrect arguments provided, expecting {str(envs)} but got {None if len(sys.argv) <= 1 else sys.argv[1]}"
        )
    dotenv_file = find_dotenv(script_dir, env)
    dotenv.load_dotenv(dotenv_file)
    return env


def find_dotenv(starting_directory, config_env=None):
    if not os.path.isdir(starting_directory):
        raise ValueError(
            f"The provided path '{starting_directory}' is not a valid directory."
        )
    current_directory = starting_directory
    while True:
        dotenv_path = os.path.join(
            current_directory, f".env.{config_env}" if config_env else ".env"
        )
        if os.path.isfile(dotenv_path):
            logging.debug(f"env file found at: {dotenv_path}")
            return dotenv_path
        if os.path.dirname(current_directory) == current_directory:
            raise FileNotFoundError(
                "'.env' file not found in any of the parent directories."
            )
        current_directory = os.path.dirname(current_directory)

"""
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
"""

import logging
import sys

from copilot.copilot_shared import process_env
from copilot.logging_service import LoggingService


def main():
    process_env()
    LoggingService.configure_logging()
    actions = []
    for plugin in ActionProvider.plugins:
        actions.append(plugin())
    for action in actions:
        action.perform()


class PluginMount(type):
    ignore_cls = ["ActionProvider"]

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if not hasattr(cls, "plugins"):
            cls.plugins = []
        if name not in PluginMount.ignore_cls:
            cls.plugins.append(cls)


class ActionProvider(metaclass=PluginMount):
    pass


class Insert(ActionProvider):
    def perform(self):
        logging.info("Insert")


class Update(ActionProvider):
    def perform(self):
        logging.info("Update")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"main caught exception: {e}", exc_info=e)
        sys.exit(1)

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
import logging
import sys

from copilot.copilot_shared import configure_logging, process_env


def main():
    process_env()
    configure_logging()
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

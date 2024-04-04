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

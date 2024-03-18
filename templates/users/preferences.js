/*
Copyright (c) 2024 eContriver LLC
This file is part of Capital Copilot from eContriver.

Capital Copilot from eContriver is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License, or any later
version.

Capital Copilot from eContriver is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
for more details.

You should have received a copy of the GNU General Public License along with Capital Copilot from eContriver.
If not, see <https://www.gnu.org/licenses/>.
*/

var userPreferences = {
    darkMode: {{ user_preferences.dark_mode|yesno:"true,false" }},
    isAuthenticated: {{ user_preferences.is_authenticated|yesno:"true,false" }},
    // Connect to data in views.py
};


/*
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
*/

var userPreferences = {
    darkMode: {{ user_preferences.dark_mode|yesno:"true,false" }},
    isAuthenticated: {{ user_preferences.is_authenticated|yesno:"true,false" }},
    // Connect to data in views.py
};


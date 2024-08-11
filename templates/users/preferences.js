/*
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
*/

var userPreferences = {
    darkMode: {{ user_preferences.dark_mode|yesno:"true,false" }},
    isAuthenticated: {{ user_preferences.is_authenticated|yesno:"true,false" }},
    // Connect to data in views.py
};


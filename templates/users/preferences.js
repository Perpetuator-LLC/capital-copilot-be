var userPreferences = {
    darkMode: {{ user_preferences.dark_mode|yesno:"true,false" }},
    isAuthenticated: {{ user_preferences.is_authenticated|yesno:"true,false" }},
    // Connect to data in views.py
};


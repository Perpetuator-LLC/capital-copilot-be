/*
Copyright (c) 2024 Perpetuator LLC

This file is part of Capital Copilot by Perpetuator LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
*/

function darkMode() {
        return {
            dark: localStorage.getItem('darkMode') === 'true' || userPreferences.darkMode || false,
            noTransition: true, // disable slider transition on page load
            init() {
                if (this.isUserAuthenticated()) {
                    this.dark = userPreferences.darkMode;
                    localStorage.setItem('darkMode', this.dark);
                } else {
                    this.dark = localStorage.getItem('darkMode') === 'true' || false;
                }
                this.$nextTick(() => {
                    this.noTransition = false;
                });
                document.documentElement.classList.toggle('dark', this.dark);
                this.$watch('dark', newVal => this.handleDarkModeChange(newVal));
            },
            toggleDarkMode() {
                this.dark = !this.dark;
            },
            updateDarkModePreference(dark) {
                fetch('/set_dark_mode/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': this.getCSRFToken(),
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: `darkMode=${dark}`,
                });
            },
            handleDarkModeChange(newVal) {
                localStorage.setItem('darkMode', newVal);
                document.documentElement.classList.toggle('dark', newVal);
                if (userPreferences.isAuthenticated) {
                    this.updateDarkModePreference(newVal);
                }
            },
            getCSRFToken() {
                const cookies = document.cookie.split(';');
                for (let cookie of cookies) {
                    const [name, value] = cookie.split('=');
                    if (name.trim() === 'csrftoken') {
                        return value;
                    }
                }
                return '';
            },
            isUserAuthenticated() {
                return userPreferences.isAuthenticated;
            }
        }
    }

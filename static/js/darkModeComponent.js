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

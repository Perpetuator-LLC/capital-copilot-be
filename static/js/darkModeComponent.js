function darkMode() {
    return {
        init() {
            this.$watch('dark', () => {
                localStorage.setItem('darkMode', this.dark);
                this.updateDarkModePreference(this.dark);
                if (this.dark) {
                    document.documentElement.classList.add('dark');
                } else {
                    document.documentElement.classList.remove('dark');
                }
            });

            if (localStorage.getItem('darkMode') === 'true') {
                this.dark = true;
            }
        },
        dark: false,
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
        getCSRFToken() {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                const [name, value] = cookie.split('=');
                if (name.trim() === 'csrftoken') {
                    return value;
                }
            }
            return '';
        }
    }
}

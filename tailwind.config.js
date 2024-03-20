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

/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // or 'media' or 'class'
  content: [
    './templates/**/*.html',
    './templates/*.html',
    './src/**/*.css',
    './src/*.css',
  ],
  theme: {
    extend: {
      colors: {
        'page-bg': '#a8a29e',
        'page-bg-dark': '#1c1917',
        'page-text': '#1c1917',
        'page-text-dark': '#a8a29e',
        'form-bg': '#dddddd',
        'form-bg-dark': '#333333',
        'form-border': '#cccccc',
        'form-border-dark': '#555555',
        'form-text': '#333333',
        'form-text-dark': '#ffffff',
        'form-button': '#333333',
        'form-button-dark': '#222222',
        'form-h1-text': '#222222',
        'form-h1-text-dark': '#ffffff',
        'form-h2-text': '#444444',
        'form-h2-text-dark': '#bbbbbb',
      }
    },
  },
  plugins: [],
  variants: {
    extend: {
      backgroundColor: ['dark'], // Ensure you have the 'dark' variant enabled for backgroundColor
      textColor: ['dark'], // And for textColor
      // Add other variants as needed
    }
  },
}


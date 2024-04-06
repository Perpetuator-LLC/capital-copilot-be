/*
Copyright (c) 2024 eContriver LLC

This file is part of Capital Copilot by eContriver LLC and is released under the MIT License.
See the LICENSE file in the root of this project for the full license text.
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


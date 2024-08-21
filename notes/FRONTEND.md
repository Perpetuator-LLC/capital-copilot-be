NOTE: This is all wrong now with front-end and back-end separation.

# Overview of Front-End Development

The tools we use:

- Alpine.js
- Tailwind CSS
- TradingView Lightweight Charting Library

## Alpine.js

Alpine.js is a minimal framework for composing JavaScript behavior in your markup. It offers you the reactive and
declarative nature of big frameworks like Vue or React at a much lower cost.

We use a CDN.

## Tailwind CSS

Tailwind CSS is a highly customizable, low-level CSS framework that gives you all of the building blocks you need to
build bespoke designs without any annoying opinionated styles you have to fight to override.

We combine it with the JIT compiler and purge unused CSS.

## TradingView Lightweight Charting Library

The TradingView Lightweight Charting Library is the best choice for you if you want to display financial data as an
interactive chart on your web page without affecting your web page loading speed and performance.

# Tailwind CSS

Tailwind CSS relies on PostCSS, a tool for transforming CSS with JavaScript, which requires Node.js.

## Setup

```shell
nvm install --lts
nvm use 20.11.1
npm install -g npm@10.5.0
npm init -y
npm install tailwindcss postcss autoprefixer
npx tailwindcss init
```

## Configuration

In the `package.json` file, add the following scripts:

```json
"scripts": {
  "build:css": "tailwindcss build -i src/styles.css -o static/css/styles.css --minify",
  "watch:css": "tailwindcss build -i src/styles.css -o static/css/styles.css --watch"
}
```

We use dark mode, so we need to configure the `tailwind.config.js` file:

```javascript
module.exports = {
  darkMode: 'class',
  theme: {
    extend: {},
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
```

In the `src/styles.css` file, add the following:

```css
@import 'tailwindcss/base';
@import 'tailwindcss/components';
@import 'tailwindcss/utilities';
```

## Integration

In the `template/base.html` file, add the following:

```html
{% load static %}
...
<link href="{% static 'css/styles.css' %}" rel="stylesheet">
```

## Usage

To build the CSS:

```shell
npm run build:css
```

To watch the CSS:

```shell
npm run watch:css
```

This will watch the `src/styles.css` file and rebuild the `static/css/styles.css` file whenever it changes.

# Icons

Go here and copy the SVG:

- https://lucide.dev/icons/menu

Style it with Tailwind CSS.

# Font

Heading font: Montserrat

Content font: Raleway

Code font: Source Code Pro

These are loaded in base.html directly from Google CDN.

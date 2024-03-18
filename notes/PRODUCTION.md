# Static Site Generation

As part of the production deployment process we need to run:

```shell
python manage.py collectstatic
```

## CSS

We are using Tailwind CSS, so we need to run:

```shell
npm run build:css
```

### Minimal CSS - WIP

We are using a minimal CSS file to style the site. We are using Tailwind CSS to generate the CSS file. We are using the JIT compiler and purging unused CSS.

```shell
npm install cssnano
...?
```

May want to research using `whitenoise` to better serve static files in production too.

## i18n 

To compile messages for translation we need to run:

```shell
python manage.py makemessages -l es
python manage.py compilemessages
```

# Tailwind CSS

Right now we are using a CDN version, but that is bulky. To speed up loadtimes we should use the JIT compiler and purge unused CSS.
- however the cached version might be faster, we will have to check

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

We are using a minimal CSS file to style the site. We are using Tailwind CSS to generate the CSS file. We are using the
JIT compiler and purging unused CSS.

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

# Django Production

See: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

## Django Debug in Container

To see the logs and follow:

```shell
docker-compose logs -f
```

```shell
docker exec -it copilot_django sh
```

## Django Admin Setup

For the initial setup of the Django admin we need to run:

```shell
docker exec copilot_django poetry run python manage.py migrate
```

To create the super user you need a TTY, so you need to run:

```shell
docker exec -it copilot_django sh
poetry run python manage.py createsuperuser
```

Once you login as the super user you need update the site to be perpetuator.com and then add the social applications for
GitHub and Google, make sure to link them to the site.

## Django Check

```shell
docker exec copilot_django poetry run python manage.py check --deploy
```

# Docker Compose Invocation

```shell
COPILOT_NGINX_PORT=3321 docker-compose up -d --build
```

# Back-up

To back-up the database we need to run:

```shell
cp db.sqlite3{,-$(date +%Y%m%d)}
```

The `.env` file should be backed up too.

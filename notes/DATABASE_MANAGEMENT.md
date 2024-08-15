# Test DB

While testing you will need to setup your database. You can use the following commands to create a test database and
user.

## Clean

```bash
mv ../db.sqlite3{,.bak}
```

## Create DB

```bash
python manage.py makemigrations
python manage.py migrate
```

## Create User

```bash
$ python manage.py createsuperuser
Username (leave blank to use 'user'): user
Email address: user@example.com
Password: 
Password (again): 
Superuser created successfully.
```

## Run Server

```bash
python manage.py runserver
```

## Access Admin

- Go to [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

# Run Server

To run the server use:

```shell
python manage.py migrate
python manage.py runserver
```

# Database

To connect to the database use:

```shell
python manage.py dbshell
```

```sqlite
sqlite> .tables
account_emailaddress           django_content_type          
account_emailconfirmation      django_migrations            
auth_group                     django_session               
auth_group_permissions         django_site                  
auth_permission                socialaccount_socialaccount  
auth_user                      socialaccount_socialapp      
auth_user_groups               socialaccount_socialapp_sites
auth_user_user_permissions     socialaccount_socialtoken    
django_admin_log        
```

# Routes

To see the routes use (command comes from `django-extensions`):

```shell
python manage.py show_urls
```

# Squash Migrations

This flow is not recommended for production environments. It's useful for development and testing. The value of this
flow is that we don't have to migrate data for empty columns etc. in development. We only need to worry about data
migration in production environments.

To accomplish this, during development, we can reset the migrations and the database. But once we go to production, then
the migrations are checked in, and we don't reset them. We then migrate on top of those, and we can keep squashing the
migrations to keep the number of migrations low until we again deploy to production.

To reset migrations use:

```shell
cd ..
mv users/migrations{,-old}
cp db.sqlite3{,-old}
python manage.py makemigrations users
python manage.py migrate --fake users zero
```

If all is good, then:

```shell
cd ..
python manage.py migrate --fake
```

If there are problems, then we can restore the old migrations and database:

```shell
mv users/migrations{-old,}
mv db.sqlite3{-old,}
```

Once we are done with development, we can remove the old migrations and database:

```shell
rm -rf users/migrations-old
rm -f db.sqlite3-old
```

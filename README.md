

# Installation
## OS Prerequisites
### Ubuntu
```shell
sudo apt install python3-dev libpq-dev gcc
```
## Python Virtual Environment
```shell
python3 -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install -e .
```
## Postgresql
### Ubuntu
* Install postgresql
```shell
sudo apt install postgresql-12
```
* Configure postgresql
```shell
sudo -u postgres psql
```
From the psql prompt:
```postgresql
CREATE DATABASE mpd;
CREATE USER mpduser WITH ENCRYPTED PASSWORD 'mpdpassword';
ALTER ROLE mpduser SET client_encoding TO 'utf8';
ALTER ROLE mpduser SET default_transaction_isolation TO 'read committed';
ALTER ROLE mpduser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mpd TO mpduser;
\q
```
* Update Django settings (mpd_django/settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mpd',
        'USER': 'mpduser',
        'PASSWORD': 'mpdpassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

## Set up initial admin account
* Add admin user
```shell
./manage.py createsuperuser
```
Enter admin username and password when prompted

# Deployment
Based on articles:
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/uwsgi/
https://medium.com/all-about-django/deploying-django-applications-in-production-with-uwsgi-and-nginx-78aac8c0f735
* Copy project to deployment directory
```shell
sudo mkdir /srv/mpd
cd /srv/mpd
git clone git@github.com:jimshepherd/mpd-django.git
git clone git@github.com:jimshepherd/mpd-react.git
```
* Install and set up mpd-django following instructions above



# Notes
* To make the django app available to remote computers
Add address of computer django on which django is running to the ALLOWED_HOSTS entry in .env
```shell
./manage.py runserver 0.0.0.0:8000
```
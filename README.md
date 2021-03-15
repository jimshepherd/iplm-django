

# Installation
## OS Prerequisites
### Ubuntu
```shell
sudo apt install python3-dev libpq-dev
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

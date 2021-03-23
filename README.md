

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
* Create mpd user (optional)
  ```shell
   sudo adduser mpd
  ```
* Copy project to deployment directory
  As mpd user
  ```shell
  sudo mkdir /srv/mpd
  sudo chown mpd.www-data /srv/mpd
  sudo chmod g+s /srv/mpd
  cd /srv/mpd
  git clone https://github.com/jimshepherd/mpd-django.git
  ```
* Install and set up mpd-django as mpd user
  ```shell
  cd mpd-django/
  python3 -m venv venv
  . venv/bin/activate
  python -m pip install --upgrade pip setuptools
  pip install -e .deploy
  ```
  This command will make sure the deployment dependencies are installed
* Update parameters in mpd_django/.env for local environment
* Set up daphne
  ```shell
  sudo cp deployment/daphne.service /etc/systemd/system/
  sudo systemctl enable --now daphne.service
  ```
  Check that the daphne service started correctly
  ```shell
  systemctl status daphne.service
  ```
* Set up nginx
  ```shell
  sudo cp deployment/mpd.conf /etc/nginx/sites-available/
  sudo ln -s /etc/nginx/sites-available/mpd.conf /etc/nginx/sites-enabled/
  sudo service nginx restart
  ```
  Check that the nginx service started correctly
  ```shell
  systemctl status nginx.service
  ```

# Update Deployment
  Run the deploy shell script as mpd user
  ```shell
  ./deployment/deploy.sh
  ```

# Notes
* To make the django app available to remote computers
Add address of computer django on which django is running to the ALLOWED_HOSTS entry in .env
```shell
./manage.py runserver 0.0.0.0:8000
```
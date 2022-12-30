

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
CREATE DATABASE iplm;
CREATE USER iplmuser WITH ENCRYPTED PASSWORD 'iplmpassword';
ALTER ROLE iplmuser SET client_encoding TO 'utf8';
ALTER ROLE iplmuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE iplmuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE iplm TO iplmuser;
\q
```
* Update Django settings (iplm/settings.py)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'iplm',
        'USER': 'iplmuser',
        'PASSWORD': 'iplmpassword',
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
* Create iplm user (optional)
  ```shell
   sudo adduser iplm
  ```
* Copy project to deployment directory
  As iplm user
  ```shell
  sudo mkdir /srv/iplm
  sudo chown iplm.www-data /srv/iplm
  sudo chmod g+s /srv/iplm
  cd /srv/iplm
  git clone https://github.com/jimshepherd/iplm-django.git
  ```
* Install and set up iplm-django as iplm user
  ```shell
  cd iplm-django/
  python3 -m venv venv
  . venv/bin/activate
  python -m pip install --upgrade pip setuptools
  pip install -e .deploy
  ```
  This command will make sure the deployment dependencies are installed
* Update parameters in iplm/.env for local environment
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
  sudo cp deployment/iplm.conf /etc/nginx/sites-available/
  sudo ln -s /etc/nginx/sites-available/iplm.conf /etc/nginx/sites-enabled/
  sudo service nginx restart
  ```
  Check that the nginx service started correctly
  ```shell
  systemctl status nginx.service
  ```

# Update Deployment
  Run the deploy shell script as iplm user
  ```shell
  ./deployment/deploy.sh
  ```

# Notes
* To make the django app available to remote computers
Add address of computer django on which django is running to the ALLOWED_HOSTS entry in .env
```shell
./manage.py runserver 0.0.0.0:8000
```

# Deploy on Google Cloud
* Follow instructions at https://cloud.google.com/python/django/run
* 
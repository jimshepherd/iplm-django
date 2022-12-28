# Update the local files
git fetch
git pull

# Update the iplm installation
. venv/bin/activate
pip install -e .deploy

# Update the database and generate the static files
./manage.py migrate
./manage.py collectstatic

# Restart the daphne service
sudo service daphne restart

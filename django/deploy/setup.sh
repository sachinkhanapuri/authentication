#!/usr/bin/env bash
set -e

PROJECT_GIT_URL="https://github.com/sachinkhanapuri/authentication.git"

PROJECT_BASE_PATH="/home/ubuntu/django"

echo "installing dependencies..."
apt-get update
apt-get install -y python3-dev python3-venv sqlite python-pip supervisor nginx git

mkdir -p $PROJECT_BASE_PATH/env
python3 -m venv $PROJECT_BASE_PATH/env

$PROJECT_BASE_PATH/env/bin/pip install -r $PROJECT_BASE_PATH/requirement.txt
$PROJECT_BASE_PATH/env/bin/pip install uwsgi==2.0.18

cd $PROJECT_BASE_PATH
$PROJECT_BASE_PATH/env/bin/python manage.py migrate
$PROJECT_BASE_PATH/env/bin/python manage.py collectstatic --noinput

cp $PROECT_BASE_PATH/deploy/supervisor_techroboproject.conf /etc/supervisor/conf.d/techroboproject.conf
supervisorctl reread
supervisorctl update
supervisorctl restart techroboproject/authrestapi

cp $PROJECT_BASE_PATH/deploy/nginx_techroboproject.conf /etc/nginx/sites-available/techroboproject.conf
rm /etc/nginx/sites-enabled/default
ln -s /etc/nginx/sites-available/techroboproject.conf /etc/nginx/sites-enabled/techroboproject.conf

echo "DONE...."
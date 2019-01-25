#!/bin/bash
# Remove any existing httpd data
rm -rf /run/httpd/* /tmp/httpd*

source "/app/bin/activate"

export DATABASE_NAME=`echo $BRANCH | sed 's/-/_/g' `
echo $DATABASE_NAME

if [ "$DB" = "mysql" ] && [ "$ENV" = "dev" ]
then
  mysql -u $DATABASE_USERNAME -p$DATABASE_PASSWORD -h $DATABASE_HOSTNAME --execute="create database $DATABASE_NAME "
fi

python manage.py migrate

pip install -r requirements.txt

rm -rf /static/
python manage.py collectstatic

# Start Apache server in foreground
exec /usr/sbin/apachectl -DFOREGROUND

#!/bin/bash

if [ "$ENV"  = "localdev" ]
then

  echo "Waiting for postgres..."

  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"

  source "/app/bin/activate"

  cd /app

  python manage.py migrate
  python manage.py initialize_person_db

  python manage.py loaddata --app coursedashboards --database uw_person \
      person.json student.json transcript.json

  python manage.py loaddata --app coursedashboards --database default \
      course.json course_offering.json instructor.json major.json \
      registration.json student_major.json term.json user.json

fi

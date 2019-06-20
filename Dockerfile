FROM acait/django-container:master

USER root
RUN apt-get update && apt-get install mysql-client libmysqlclient-dev libapache2-mod-wsgi libxmlsec1-dev -y

ADD --chown=acait:acait coursedashboards/VERSION /app/coursedashboards/
ADD --chown=acait:acait setup.py /app/
ADD --chown=acait:acait requirements.txt /app/
RUN . /app/bin/activate && pip install -r requirements.txt
RUN . /app/bin/activate && pip install mysqlclient

RUN . /app/bin/activate && pip install nodeenv && nodeenv -p &&\
    npm install -g npm &&\
    ./bin/npm install less -g

ADD --chown=acait:acait . /app/
ADD --chown=acait:acait docker/ /app/project/
ADD --chown=acait:acait docker/app_start.sh /scripts
RUN chmod u+x /scripts/app_start.sh

RUN . /app/bin/activate && python manage.py compress -f && python manage.py collectstatic --noinput

USER acait
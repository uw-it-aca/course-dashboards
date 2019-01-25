FROM acait/django-container:python2
RUN apt-get update && apt-get install mysql-client libapache2-mod-wsgi -y
RUN mkdir /app/logs
ADD coursedashboards/VERSION /app/myuw/
ADD setup.py /app/
ADD requirements.txt /app/
ADD . /app/
RUN . /app/bin/activate && pip install -r requirements.txt
ADD /docker/web/apache2.conf /tmp/apache2.conf
RUN rm -rf /etc/apache2/sites-available/ && mkdir /etc/apache2/sites-available/ && \
    rm -rf /etc/apache2/sites-enabled/ && mkdir /etc/apache2/sites-enabled/ && \
    rm /etc/apache2/apache2.conf && \
    cp /tmp/apache2.conf /etc/apache2/apache2.conf &&\
    mkdir /etc/apache2/logs
ENV DB sqlite3
ADD docker /app/project/
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh" ]

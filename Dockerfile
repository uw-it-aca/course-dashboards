FROM acait/django-container:python2
RUN apt-get update && apt-get install mysql-client libapache2-mod-wsgi libxmlsec1-dev -y
ADD /docker/web/apache2.conf /tmp/apache2.conf
ADD docker/web/start.sh /start.sh
RUN chmod +x /start.sh
RUN rm -rf /etc/apache2/sites-available/ && mkdir /etc/apache2/sites-available/ && \
    rm -rf /etc/apache2/sites-enabled/ && mkdir /etc/apache2/sites-enabled/ && \
    rm /etc/apache2/apache2.conf && \
    cp /tmp/apache2.conf /etc/apache2/apache2.conf &&\
    mkdir /etc/apache2/logs
RUN mkdir /static
RUN mkdir /app/logs
RUN useradd -g root aca
RUN chown -R aca:root /app && chown -R aca:root /static && chown -R aca:root /run
USER aca
WORKDIR /app
ADD coursedashboards/VERSION /app/coursedashboards/
ADD setup.py /app/
ADD requirements.txt /app/
ADD . /app/
RUN . /app/bin/activate && pip install -r requirements.txt
ENV DB sqlite3
WORKDIR /app
ADD docker /app/project/
CMD ["/start.sh" ]

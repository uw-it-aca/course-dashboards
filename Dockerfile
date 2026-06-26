ARG DJANGO_CONTAINER_VERSION=3.1.1

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-container:${DJANGO_CONTAINER_VERSION} AS app-container

COPY --chown=acait:acait . /app/
COPY --chown=acait:acait docker/ /app/project/

COPY --chown=acait:acait docker/app_start.sh /scripts
RUN chmod u+x /scripts/app_start.sh

RUN /app/bin/pip install -r requirements.txt
RUN /app/bin/pip install "psycopg[c,pool]"

RUN . /app/bin/activate && pip install nodeenv && nodeenv -p && \
    npm install -g npm && ./bin/npm install less -g

RUN . /app/bin/activate && python manage.py collectstatic --noinput && \
  python manage.py compress -f

FROM us-docker.pkg.dev/uwit-mci-axdd/containers/django-test-container:${DJANGO_CONTAINER_VERSION} AS app-test-container

USER root

RUN apt-get update && apt-get install sqlite3 -y

USER acait

COPY --from=app-container /app/ /app/

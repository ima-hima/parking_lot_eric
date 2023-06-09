FROM python:3.9-alpine3.13
LABEL maintainer="eric"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./parking_lot /parking_lot
WORKDIR /parking_lot
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    # Following are dependencies for psycopg2 on Alpine.
    # --virtual makes a virtual dependency directory, for easier
    # removal later.
    # apk is Alpine package manager.
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
    chown -R django-user:django-user /parking_lot && \
    chmod -R 755 /parking_lot

ENV PATH="/py/bin:$PATH"

USER django-user

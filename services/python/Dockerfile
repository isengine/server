FROM python:3.11-alpine

WORKDIR /var/www

RUN apk update && apk add bash
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev && \
  pip install --no-cache-dir -r requirements.txt

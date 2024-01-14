FROM python:3-slim

WORKDIR /var/www
# WORKDIR /var/www/example.com

RUN apt-get update && apt-get install -y bash gcc

RUN rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install flask
RUN pip install gunicorn

# RUN pip install --no-cache-dir -r requirements.txt

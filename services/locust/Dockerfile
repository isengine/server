FROM python:3-slim

WORKDIR /var/www

RUN apt-get update && apt-get install -y bash gcc

RUN rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install locust

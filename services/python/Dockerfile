FROM python:3-slim

WORKDIR /usr/src/app

RUN apt-get update && \
apt-get install bash && \
apt-get install -y gcc && \
rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install gunicorn

COPY ./data/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

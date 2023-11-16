FROM python:3.9-slim

# Создаём отдельного пользователя для запуска кода
RUN useradd -rm -d /home/student -s /bin/bash -u 1001 student

# Установим Golang, ведь нам предстоит компилировать и запускать код на Go!
RUN apt-get update && \
apt-get install -y -q --no-install-recommends golang && \
rm -rf /var/lib/apt/lists/

# Установим C++
# ENV GCC_VERSION 10.2.1-1

RUN apt-get update && \
apt-get install -y --no-install-recommends gcc gcc-multilib g++ && \
rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip
RUN pip install aiohttp
RUN pip install serverhub_agent

WORKDIR /app

FROM python:3.9-slim

RUN pip install --no-cache-dir --upgrade pip && \
    pip install aiohttp aiohttp_cors serverhub_agent \
                matplotlib numpy opencv-python opencv-python-headless \
                tensorflow ultralytics

# Создаём отдельного пользователя для запуска кода
RUN useradd -rm -d /home/student -s /bin/bash -u 1001 student

# Установим библиотеки для языков
# Go C++ Node.js
RUN apt-get update && \
    apt-get install -y -q --no-install-recommends \
    htop \
    golang \
    gcc gcc-multilib g++ \
    nodejs npm yarn && \
    rm -rf /var/lib/apt/lists/*

# RUN npm install -g typescript @types/node @babylonjs/core

WORKDIR /app

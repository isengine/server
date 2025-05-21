FROM python:3.12

RUN apt update \
    && apt install -y --no-install-recommends \
        bash \
        build-essential \
        cmake \
        curl \
        gcc gcc-multilib g++ \
        git \
        libglib2.0-0 \
        software-properties-common \
        wget

RUN rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip

RUN pip install aiohttp aiohttp_cors
# RUN pip install evaluate
RUN pip install fastapi
RUN pip install flask
RUN pip install gradio
RUN pip install gunicorn
RUN pip install matplotlib
RUN pip install numpy
RUN pip install opencv-python opencv-python-headless
RUN pip install pandas
# RUN pip install transformers
# RUN pip install torch
# RUN pip install selenium webdriver-manager
RUN pip install serverhub_agent
RUN pip install ultralytics

# RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /var/www

FROM python:3.12

WORKDIR /app

# установка зависимостей
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

# драйвера для nvidia или для amd нужно ставить снаружи, а контейнер увидит их за счет настроек с пробросом gpu

RUN python -m pip install --upgrade pip

RUN pip install \
    fastapi \
    torch \
    torchvision \
    git+https://github.com/huggingface/transformers \
    git+https://github.com/huggingface/accelerate \
    pydantic \
    qwen-vl-utils \
    serverhub_agent \
    uvicorn

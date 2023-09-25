FROM php:8-fpm-alpine

# https://wiki.alpinelinux.org/wiki/Setting_the_timezone
# RUN echo "${WORKSPACE_TIMEZONE}" && apk --update add tzdata && \
#     cp /usr/share/zoneinfo/$WORKSPACE_TIMEZONE /etc/localtime && \
#     echo $WORKSPACE_TIMEZONE > /etc/timezone && \
#     apk del tzdata

RUN apk add --no-cache -f acl \
    bash \
    build-base \
    composer \
    freetype \
    gettext-dev \
    git \
    gmp-dev \
    icu \
    libcurl \
    libintl \
    libjpeg-turbo \
    libpng \
    libwebp \
    libxml2-dev \
    libzip \
    msmtp \
    mysql-client \
    oniguruma-dev \
    openssh-client \
    patch \
    pcre-dev \
    perl \
    postgresql-dev \
    procps \
    shadow \
    su-exec \
    unzip \
    vim \
    wget \
    zip \
    zlib

RUN apk add --update --no-cache --virtual build-essentials \
    autoconf \
    automake \
    freetype-dev \
    g++ \
    htop \
    icu-dev \
    icu-libs \
    libjpeg-turbo-dev \
    libpng-dev \
    libwebp-dev \
    libzip-dev \
    make \
    nodejs \
    npm \
    supervisor \
    zlib-dev

RUN docker-php-ext-configure gd --enable-gd --with-freetype --with-jpeg --with-webp && \
    docker-php-ext-configure gettext && \
    docker-php-ext-configure intl && \
    docker-php-ext-configure opcache --enable-opcache && \
    docker-php-ext-configure pcntl --enable-pcntl && \
    docker-php-ext-configure soap

RUN docker-php-ext-install exif \
    gd \
    gettext \
    gmp \
    intl \
    mysqli \
    opcache \
    opcache \
    pcntl \
    pdo_mysql \
    pdo_pgsql \
    soap \
    xml \
    zip

RUN apk del build-essentials && rm -rf /usr/src/php*

RUN apk add --no-cache $PHPIZE_DEPS

RUN pecl install -o -f redis mongodb \
    && rm -rf /tmp/pear

RUN docker-php-ext-enable mongodb && \
    docker-php-ext-enable redis

RUN rm -rf /var/cache/apk/* && docker-php-source delete

RUN php -i Session Support => enabled

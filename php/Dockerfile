FROM php:8-fpm-alpine

RUN apk update && apk add -f bash \
    git \
    curl \
    zip \
    vim \
    unzip \
    composer \
    openssh \
    libpq-dev \
    icu \
    icu-dev \
    icu-libs \
    libjpeg-turbo-dev \
    libpng-dev \
    libwebp-dev \
    freetype-dev \
    libzip-dev \
    zlib

RUN apk update

RUN docker-php-ext-install pdo \
    pgsql \
    pdo_pgsql \
    mysqli \
    pdo_mysql \
    bz2 \
    ctype \
    fileinfo \
    ftp \
    gd \
    intl \
    pcntl \
    phar \
    posix \
    zip

RUN docker-php-ext-configure gd --with-jpeg --with-webp --with-freetype

# RUN apk add --no-cache bash mysql-client msmtp perl wget procps shadow libzip libpng libjpeg-turbo libwebp freetype icu \
#     libintl patch acl git gettext-dev libcurl libxml2-dev openssh-client pcre-dev su-exec build-base oniguruma-dev \
#     gmp-dev postgresql-dev gettext gettext-dev
# 
# RUN apk add --update --no-cache --virtual build-essentials \
#     icu-dev icu-libs zlib-dev g++ make automake autoconf libzip-dev \
#     htop supervisor nodejs npm \
#     libpng-dev libwebp-dev libjpeg-turbo-dev freetype-dev && \
#     docker-php-ext-configure gd --enable-gd --with-freetype --with-jpeg --with-webp && \
#     docker-php-ext-configure gettext && \
#     docker-php-ext-configure opcache --enable-opcache && \
#     docker-php-ext-configure pcntl --enable-pcntl && \
#     docker-php-ext-configure soap && \
#     docker-php-ext-configure intl && \
#     docker-php-ext-install intl && \
#     docker-php-ext-install gettext && \
#     docker-php-ext-install pcntl && \
#     docker-php-ext-install gd && \
#     docker-php-ext-install opcache && \
#     docker-php-ext-install soap && \
#     docker-php-ext-install xml && \
#     docker-php-ext-install gmp && \
#     docker-php-ext-install exif && \
#     docker-php-ext-install zip && \
#     apk del build-essentials && rm -rf /usr/src/php*
# 
# RUN apk add --no-cache $PHPIZE_DEPS
# RUN pecl install -o -f redis mongodb \
#     &&  rm -rf /tmp/pear \
#     &&  docker-php-ext-enable redis \
#     &&  docker-php-ext-enable mongodb
# 
# # Clean
# RUN rm -rf /var/cache/apk/* && docker-php-source delete
# 
# USER root
# 
# RUN curl -sS https://getcomposer.org/installer | php
# RUN mv composer.phar /usr/local/bin/composer
# RUN /usr/local/bin/composer self-update
# 
# USER www-data:www-data
# 
# WORKDIR /var/www/
# 
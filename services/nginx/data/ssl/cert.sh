#!/usr/bin/bash

path=$PWD
domain=$DOMAIN
email=$EMAIL

apt install certbot

certbot certonly --agree-tos -m $email --webroot -w /var/www/$domain -d $domain
certbot renew --dry-run

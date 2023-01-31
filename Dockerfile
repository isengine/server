FROM node:lts-alpine

WORKDIR /var/www
COPY package*.json ./
RUN yarn
RUN apk update && apk add bash
COPY . .
EXPOSE 8080

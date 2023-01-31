FROM node:lts-alpine

WORKDIR /var/www
COPY package*.json ./
RUN yarn global add @quasar/cli
RUN apk update && apk add bash
COPY . .
EXPOSE 8080

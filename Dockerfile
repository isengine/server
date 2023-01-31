FROM node:lts-alpine

WORKDIR /var/www
RUN apk update && apk add bash
COPY package*.json ./
RUN yarn global add @quasar/cli
RUN yarn
COPY . .
EXPOSE 8080

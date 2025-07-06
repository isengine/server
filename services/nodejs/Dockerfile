FROM node:lts-alpine

RUN cd /home/node

RUN apk update && apk add bash yarn

RUN yarn global add @quasar/cli 

RUN apk add openjdk17
RUN apk add openjdk21

# RUN wget https://dl.google.com/android/repository/tools_r25.2.3-linux.zip
# RUN unzip tools_r25.2.3-linux.zip -d sdk

RUN wget https://dl.google.com/android/repository/tools_r34.0.0-linux.zip
RUN unzip tools_r34.0.0-linux.zip -d sdk

RUN wget https://dl.google.com/android/repository/tools_r35.0.0-linux.zip
RUN unzip tools_r35.0.0-linux.zip -d sdk

RUN cd sdk/tools

RUN ./android update sdk --no-ui

RUN export PATH=${PATH}:$ANDROID_HOME/platform-tools:$ANDROID_HOME/tools:$ANDROID_HOME/build-tools/26.0.0-preview/

# RUN apk add libc6:i386 libstdc++6:i386
# RUN apk add zlib1g:i386

WORKDIR /var/www

COPY . .

# apk add gcc g++ make python3
#
# echo > .bashrc
#
# nano .bashrc
# export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
# [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
FROM alvrme/alpine-android:latest-jdk21

RUN apk update
RUN apk add bash gcc g++ make python3 nodejs npm yarn
RUN yarn global add @quasar/cli 

WORKDIR /var/www

COPY . .

# sdkmanager --licenses

# npm install --save @capacitor/core @capacitor/cli
# quasar add capacitor
# quasar capacitor add android

# npm install -g cordova
# quasar mode add cordova
# quasar cordova add android

# keytool -genkey -v -keystore my-release-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias

# quasar build -m android
# quasar build -m capacitor -T android
# quasar build -m capacitor -T android --release
# quasar build -m cordova -T android
# quasar build -m cordova -T android --release

# quasar build -m capacitor -T ios --release
# quasar build -m ios

# apksigner sign --ks my-release-key.jks --ks-key-alias my-key-alias --ks-pass pass:your-keystore-password --key-pass pass:your-key-password app-release-unsigned.apk
# apksigner sign --ks my-release-key.jks --ks-key-alias my-key-alias --ks-pass pass:123456 --key-pass pass:123456 ./dist/capacitor/android/apk/release/app-release-unsigned.apk
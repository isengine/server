# Среда разработки

LDS - сокращенно от local development server, локальный сервер разработки.

Это среда для локальной разработки web-приложений, построенная на базе Docker контейнеров и linux alpine.

# Оглавление

- [Быстрый старт](#быстрый-старт)
- [О проекте](#о-проекте)
  - [Состав](#состав)
  - [Структура](#структура)
    - [Файлы](#файлы)
    - [mongo](#mongo)
    - [mysql](#mysql)
    - [nginx](#nginx)
    - [php](#php)
    - [postgres](#postgres)
    - [redis](#redis)
  - [Проблемы](#проблемы)
- [Docker](#docker)
  - [Установка под Windows](#установка-под-windows)
  - [Установка под Linux](#установка-под-linux)
  - [Команды Docker](#команды-docker)
- [Git](#git)
  - [Установка Git](#установка-git)
  - [Команды Git](#команды-git)
- [Начало работы](#начало-работы)
  - [Установка](#установка)
  - [Настройка](#настройка)
  - [Хосты](#хосты)
  - [Маршрутизация](#маршрутизация)
  - [SSH-ключи](#ssh-ключи)
  - [Результат](#результат)
  - [Запускаем контейнеры](#запускаем-контейнеры)
- [Настройка компонентов](#настройка-компонентов)
  - [Настройка nodejs](#настройка-nodejs)
  - [Настройка nginx и php](#настройка-nginx-и-php)
  - [Настройка phpMyAdmin](#настройка-phpmyadmin)
  - [Настройка MySQL](#настройка-mysql)
  - [Дамп MySQL](#дамп-mysql)
  - [Дамп PostgreSQL](#дамп-postgresql)
  - [Дамп MongoDB](#дамп-mongodb)

# Быстрый старт

Быстрый запуск в 5 простых шагов.

**1**. Перед началом, установите и настройте Docker и Git

[подробнее о Docker](#docker)
[подробнее о Git](#git)

**2**. Выполните клонирование данного репозитория в ваш проект на локальном компьютере.

```shell script
git clone https://github.com/isengine/lds
```

**3**. Удалите все файлы **.gitkeep** во всех вложенных каталогах среды разработки.

```shell script
# windows power shell
remove-item lds/* -include .gitkeep -recurse
# linux
find lds/ -name ".gitkeep" | xargs rm
```

**4**. Переместите или скопируйте файлы

```
.env
docker-compose.yml
Dockerfile
```

Из каталога **lds** среды разработки в каталог с вашим проектом.

```shell script
# windows power shell
cp lds/.env,lds/docker-compose.yml,lds/Dockerfile ./
# linux
cp lds/{.env,docker-compose.yml,Dockerfile} ./
```

**5**. Соберите проект из каталога вашего проекта

> Возможно, для корректной работы придется настроить переменные окружения, сервисы docker и связь с базой данных.

```shell script
docker-compose up --build
# с флагом -d консоль не заблокируется, но и вывод информации будет ограничен
docker-compose up --build -d
```

Дальнейшие команды для работы:

```shell script
# запуск
docker-compose start
# остановка
docker-compose stop
# подключение к контейнерам
docker-compose exec nodejs bash
docker-compose exec php bash
```

Вывод проекта через node.js на 8080 порт: http://localhost:8080

Вывод статики из каталога "./public/" через сервер nginx + php-fpm на 80 порт: http://localhost

phpMyAdmin работает на 8000 порту: http://localhost:8000

Adminer работает на 8800 порту: http://localhost:8800

> В случае необходимости изменить конфигурацию сервера, возникновения ошибок и прочих вопросов, смотрите полное руководство.

[^ к оглавлению](#оглавление)

# О проекте

## Состав

Среда разработки включает в себя следующие контейнеры и компоненты:

- nodejs
  - yarn
- nginx
- php
  - git
  - composer
- adminer
- phpmyadmin
- mysql
- redis
- postgres
- mongo

[^ к оглавлению](#оглавление)

## Структура

```
lds
├── .env
├── docker-compose.yml
├── Dockerfile
├── README.md
├── .ssh
├── mongo
├── mysql
├── nginx
├── php
├── postgres
└── redis
```

[^ к оглавлению](#оглавление)

### Файлы

**.gitkeep** - это пустые файлы, которые нужны только для того, чтобы добавить каталог под наблюдение **Git**.

**.env** - файл с основными настройками среды разработки.

**docker-compose.yml** - документ в формате YML, в котором определены правила создания и запуска многоконтейнерных приложений Docker. 

**Dockerfile** - конфигурационный файл, в котором описаны инструкции, которые будут применены при сборке Docker-образа и запуске контейнера.

**README.md** - документация.

**.ssh** - каталог для хранения ssh-ключей.

[^ к оглавлению](#оглавление)

### mongo

Каталог базы данных MongoDB.

```
├── configdb
│   └── mongo.conf
├── db
└── dump
```

**mongo.conf** — Файл конфигурации MongoDB. В этот файл можно добавлять параметры, которые при перезапуске MongoDB будут применены.

**db** — этот каталог предназначен для хранения пользовательских данных MongoDB.

**dump** — каталог для хранения дампов.  

[^ к оглавлению](#оглавление)
 
### mysql

Каталог базы данных MySQL.

```
├── conf.d
│   └── config-file.cnf
├── data
├── dump
└── logs
```

**config-file.cnf** — файл конфигурации. В этот файл можно добавлять параметры, которые при перезапуске MySQL 8 будут применены.

**data** — этот каталог предназначен для хранения пользовательских данных MySQL 8.

**dump** — каталог для хранения дампов.

**logs** — каталог для хранения логов.

[^ к оглавлению](#оглавление)

### nginx

Этот каталог предназначен для хранения файлов конфигурации Nginx и логов.

```
├── conf.d
│   ├── nginx.conf
└── logs
```

**nginx.conf** — файл конфигурации виртуальных хостов web-проектов.

```nginx
listen 80;
server_name localhost;
```

Здесь указан порт и название сервера.

```nginx
index index.php;
```

Здесь указан индексный файл, точка входа.

```nginx
error_log  /var/log/nginx/error.log;
access_log /var/log/nginx/access.log;
```

Здесь заданы каталоги и файлы отчетов о работе сервера.

```nginx
root /var/www/public;
```

Здесь задан корневой каталог проекта.

Дальше следуют другие настройки. Но нам следует обратить внимание на то, как производится перенаправление запросов к нужному docker-контейнеру.

```nginx
fastcgi_pass php:9000;
```

**php** — название docker-контейнера, а **9000** — порт внутренней сети. Контейнеры между собой связаны через внутреннюю сеть **network**, которая определена в файле **docker-compose.yml**.

Если вам нужно создать несколько параллельных проектов, вы можете их настроить, создав для каждого свою секцию

```nginx
server {
    ...
}
```

[^ к оглавлению](#оглавление)

### php

Каталог данных PHP.

```
├── supervisor.d
├── Dockerfile
└── php.ini
```

**supervisor.d** — место для хранения файлов конфигурации **Supervisor**.

**Dockerfile** — это текстовый документ, содержащий все команды, которые следует выполнить для сборки образов PHP.

**php.ini** — это файл конфигурации PHP.

[^ к оглавлению](#оглавление)

### postgres

Каталог для системы управления базами данных PostgreSQL.

```
├── .gitkeep
├── data
└── dump 
```

**data** — этот каталог предназначен для хранения пользовательских данных PostgreSQL.

**dump** — каталог для хранения дампов.

[^ к оглавлению](#оглавление)

### redis

Каталог key-value хранилища Redis.

```
├── conf
└── data
```

**conf** — каталог для хранения специфических параметров конфигурации.

**data** — если настройки конфигурации предполагают сохранения данных на диске, то Redis будет использовать именно этот каталог.

[^ к оглавлению](#оглавление)

## Проблемы

Перед началом работы рекомендуется удалить все файлы **.gitkeep** из всех вложенных каталогов. Иначе могут быть проблемы, например, с хранилищами баз данных.

Автоматическая настройка контейнера "php" невозможна из-за того, что при установке недостающих библиотек он падает в ошибку.

На текущий момент рабочее решение - настраивать его вручную. Подробные инструкции даны ниже.

Контейнер mysql не будет корректно работать под именем localhost, т.к. по-умолчанию это имя привязано к ip 127.0.0.1, а реальный ip адрес контейнера отличается. При попытке назначить данный ip адрес и открыть его наружу, контейнер падает в ошибку, т.к. возникает конфликт с системой.

На текущий момент рабочее решение - для локальной разработки использовать в вашем проекте другое имя сервера (хоста) MySQL, по-умолчанию задано "mysql".

В контейнер nodejs по-умолчанию включены команды, запускающие билд quasar. Возможно, для вашего проекта нужно будет их убрать.

[^ к оглавлению](#оглавление)

# Docker

## Установка под Windows

Для правильной работы нужен компонент WSL2.

Скачиваем и устанавливаем обновление

https://learn.microsoft.com/ru-ru/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package

Проверим его наличие и версию

```shell script
wsl -l -v
```

Должна быть 2. Если нет, то устанавливаем

```shell script
wsl --set-default-version 2
```

Затем ставим дистрибутив Linux Ubuntu

```shell script
wsl --install -d Ubuntu
```

И назначаем его по-умолчанию

```shell script
wsl --set-default Ubuntu
```

После этого устанавливаем Docker desktop с параметром "использовать WSL 2" или включаем его в настройках ("Use the WSL 2 based engine").

Запускаем.

Docker desktop под Windows по-умолчанию включает компоненты docker, docker-compose и операции для работы через командную строку.

[^ к оглавлению](#оглавление)

## Установка под Linux

Инструкция по установке и настройке docker:

https://docs.docker.com/desktop/install/linux-install/

Docker под Linux по-умолчанию НЕ включает в себя docker-compose. Поэтому ставить его нужно отдельно.

> Под Linux комманды docker нужно вводить из-под суперпользователя, например:

```shell script
sudo docker-compose up --build
```

[^ к оглавлению](#оглавление)

## Команды Docker

Сборка:

```shell script
docker-compose up --build
# с флагом -d консоль не заблокируется, но и вывод информации будет ограничен
docker-compose up --build -d
```

Полное отключение:

```shell script
docker-compose down
```

Обычный запуск:

```shell script
docker-compose run
# или
docker-compose start
```

Остановка:

```shell script
docker-compose stop
```

Подключение к контейнеру:

```shell script
docker-compose exec CONTAINER_NAME sh (или bash, если установлен)
# или
docker exec -it CONTAINER_NAME sh (или bash, если установлен)
```

Выполнить команду в контейнере:

```shell script
docker exec -it CONTAINER_NAME COMMAND
# например, посмотреть версию php из контейнера php
docker exec -it php php -v
```

Чистим докер:

```shell script
docker system prune --volumes --all
```

Список контейнеров:

```shell script
# запущенные контейнеры
docker ps
# все контейнеры
docker ps -a
```

Информация о контейнере:

```shell script
docker inspect CONTAINER_NAME
```

Перезагрузить контейнер:

```shell script
docker restart CONTAINER_NAME
```

Удалить контейнеры:

```shell script
# удаление всех контейнеров
docker rm -v $(docker ps -aq)
# удаление активных контейнеров
docker rm -v $(docker ps -q)
# удаление неактивных контейнеров
docker rm -v $(docker ps -aq -f status=exited)
```

Список образов:

```shell script
docker images
```

Удалить образы:

```shell script
docker rmi $(docker images -q)
```

[^ к оглавлению](#оглавление)

# Git

## Установка Git

Для правильной работы под Windows нужно установить приложение по ссылке

https://git-scm.com/download/win

Под Linux нужно установить пакет **git** соответствующей командой. Например:

```shell script
# ubuntu
apt-get install git
# alpine
apk add git
```

[^ к оглавлению](#оглавление)

## Команды Git

Клонировать репозиторий:

```shell script
# обычное копирование
git clone https://repository-url.git
# в текущую папку
git clone https://repository-url.git .
# с указанием ветки
git clone --branch BRANCH_NAME https://repository-url.git .
```

Выбрать ветку репозитория для дальнейшей работы:

```shell script
git branch BRANCH_NAME
```

Узнать статус:

```shell script
git status
```

Статус покажет, какие файлы изменены, но не добавлены, какие ожидают коммита и т.п.

Получить лог последних действий:

```shell script
git log
```

Посмотреть информацию и проверить подключение к репозиторию:

```shell script
git remote show origin
```

Получить последние изменения:

```shell script
git fetch origin BRANCH_NAME
git pull origin BRANCH_NAME
```

Залить свои изменения в репозиторий:

```shell script
# добавить папку или файл
git add PATH/TO/FOLER/OR/FILE.EXT
...
git commit -m "DESCRIPTION"
git push origin BRANCH_NAME
```

Отменить изменения:

```shell script
# убрать папку или файл из коммита
git restore --staged PATH/TO/FOLER/OR/FILE.EXT
# вернуть файл из репозитория
git restore PATH/TO/FILE.EXT
# отменить коммит
git revert COMMIT_ID
```

[^ к оглавлению](#оглавление)

# Начало работы

## Установка

**1**. Выполните клонирование данного репозитория в ваш проект на локальном компьютере.

```shell script
git clone https://github.com/isengine/lds
```

**2**. Удалите все файлы **.gitkeep** во всех вложенных каталогах.

```shell script
# windows power shell
remove-item * -include .gitkeep -recurse
# linux
rm -rf .gitkeep
```

**3**. Переместите или скопируйте файлы

```
.env
docker-compose.yml
Dockerfile
```

Из каталога **lds** (этой среды разработки) в каталог выше (с вашим проектом).

[^ к оглавлению](#оглавление)

## Настройка

Настройте файлы локального сервера по вашему желанию:

**1**. Удалите ненужные контейнеры в файле **docker-compose.yml**.

**2**. Задайте переменные окружения в файле **.env**.

**3**. Настройте команды после запуска nodejs в файле **Dockerfile**.

**4**. Настройте команды после запуска php в файле **Dockerfile** в каталоге **./php/**.

**5**. Отредактируйте настройки виртуальных хостов **Nginx** в файле **nginx.conf** в каталоге **./nginx/conf.d/**.

[^ к оглавлению](#оглавление)

## Хосты

Настройте хосты (доменные имена) web-проектов на локальной машине. 

Необходимо добавить названия хостов web-проектов в файл **hosts** на вашем компьютере. 

В файле **hosts** следует описать связь доменных имён ваших web-проектов в среде разработки на локальном компьютере и IP docker-контейнера **nginx**.
 
На Mac и Linux этот файл расположен в **/etc/hosts**. На Windows он находится в **C:\Windows\System32\drivers\etc\hosts**. 

Строки, которые вы добавляете в этот файл, будут выглядеть примерно так:

```
127.0.0.1   localhost
```

В данном случае, мы исходим из того, что **Nginx**, запущенный в docker-контейнере, доступен по адресу **127.0.0.1** и web-сервер слушает порт **80**.

[^ к оглавлению](#оглавление)

## Маршрутизация

По своему желанию вы можете также настроить маршрутизацию внутри контейнеров.

Web-проекты должны иметь возможность отправлять http-запросы друг другу и использовать для этого название хостов.

Из одного запущенного docker-контейнера **php** web-приложение №1 должно иметь возможность отправить запрос к web-приложению №2, которое работает внутри другого docker-контейнера **nodejs**. При этом адресом запроса может быть название хоста, которое указано в файле **/etc/hosts** локального компьютера.

Чтобы это стало возможным нужно внутри контейнеров так же внести соответствующие записи в файл **/etc/hosts**.

Самый простой способ решить данную задачу — добавить секцию **extra_hosts** в описание сервисов **php** и **nodejs** в **docker-compose.yml**.

Пример:

```
  ...  
  php:
  ...
    extra_hosts:
      - 'PROJECT_1_HOST_NAME_FROM_HOSTS:IP_HOST_MACHINE'
      - 'PROJECT_2_HOST_NAME_FROM_HOSTS:IP_HOST_MACHINE'
  ...
```

**PROJECT_х_HOST_NAME_FROM_HOSTS** — имя хоста, заданное в пункте выше.

**IP_HOST_MACHINE** — IP адрес, по которому из docker-контейнера доступен ваш локальный компьютер.

Если вы разворачиваете среду разработки на **Mac**, то внутри docker-контейнера вам доступен хост **docker.for.mac.localhost**.

Узнать **IP** адрес вашего **Mac** можно при помощи команды, который нужно выполнить на локальной машине: 

```shell script
docker run -it alpine ping docker.for.mac.localhost
```

В результате вы получите, что-то подобное:

``` 
PING docker.for.mac.localhost (192.168.65.2): 56 data bytes
64 bytes from 192.168.65.2: seq=0 ttl=37 time=0.286 ms
64 bytes from 192.168.65.2: seq=1 ttl=37 time=0.504 ms
64 bytes from 192.168.65.2: seq=2 ttl=37 time=0.801 ms
```
 
После того, как вам станет известен IP-адрес, укажите его в секции **extra_hosts** в описание сервисов **php** и **nodejs** в **docker-compose.yml**.
  
```
  php:
  ...
    extra_hosts:
      - 'php:192.168.65.2'
      - 'nodejs:192.168.65.2'
  ...
```

[^ к оглавлению](#оглавление)

## SSH-ключи

Для работы web-проектов могут потребоваться SSH-ключи, например для того, чтобы из контейнера при помощи **Composer** можно было установить пакет из приватного репозитория.

Создать SSH-ключи можно при помощи следующей команды:

```shell script
ssh-keygen -f /.ssh/id_rsa -t rsa -b 2048 -C "your-name@example.com"
```

Вместо **your-name@example.com** укажите свой email. 

В каталог **.ssh/** будут сохранены 2 файла — публичный и приватный ключ. 

Если вы скопировали в каталог **.ssh** свой ранее созданный ssh-ключ, то убедитесь, что файл **id_rsa** имеет права **700** (-rwx------@).

Установить права можно командой:
 
```shell script
chmod 700 id_rsa.
```

[^ к оглавлению](#оглавление)

## Результат

Вывод проекта через node.js на 8080 порт.

http://localhost:8080

Вывод статики из каталога "./public/" через сервер nginx + php-fpm на 80 порт.

http://localhost

phpMyAdmin работает на 8000 порту.

http://localhost:8000

Adminer работает на 8800 порту.

http://localhost:8800

[^ к оглавлению](#оглавление)

## Запускаем контейнеры

В первый раз запускаем проект с установкой необходимых образов и компонентов

```shell script
docker-compose up --build
```

С флагом -d консоль не заблокируется, но и вывод информации будет ограничен

```shell script
docker-compose up --build -d
```

Предлагаю использовать разные вкладки

Если консоль заблокирована процессом, то процесс можно остановить, нажав

```
Ctrl + C
```

Чтобы остановить процесс выполнения контейнеров с удалением контейнеров

```shell script
docker-compose down
```

[^ к оглавлению](#оглавление)

# Настройка компонентов

## Настройка nodejs

Подключимся к контейнеру

```shell script
docker exec -it nodejs bash
```

Вы можете установить зависимости, которые могут быть нужны. Например:

```shell script
yarn global add @quasar/cli
```

> Мы рекомендуем использовать **yarn** вместо **npm**.

Сборка делается автоматически при создании контейнера. Но если нужно ее повторить, можете выполнить команду

```shell script
yarn
# или
yarn install
```

Дальше остается сделать билд.

Например:

```shell script
yarn build
# или команду билда вашего проекта
# например, для фреймворка quasar на vue:
quasar dev
```

Вы можете объединить эти команды и прописать их в файл **docker-compose.yml** в секцию **nodejs**:

```
command: bash -c "quasar dev"
```

Тогда они будут выполняться сами при каждой сборке среды.

> Если контейнер nodejs не будет занят каким-либо процессом, он автоматически завершится.

[^ к оглавлению](#оглавление)

## Настройка nginx и php

В Nginx в первом volume (/var/www) подключаем статику сайта с компьютера в контейнер для публикации. Этот же volume используется для php.

Во втором volume (/etc/nginx/conf.d) - настройки самого Nginx для работы с php.

```
fastcgi_pass php:9000;
```

этой строкой Nginx понимает, где расположен сервер с php. Контейнер с php по умолчанию расположен на 9000 порту, php - это имя сервиса, которое мы задали в файле **docker-compose.yml**.

Также через настройки контейнера мы передаем в контейнер php настройки MySQL из переменных среды для подключения к базе. В php потом их можно взять из глобального массива $_ENV.

В php мы можем не просто взять image, но и произвести настройку контейнера. Установить службы для работы с MySQL, установить composer и др.

На данный момент, если делать это в автоматическом режиме, то контейнер падает с ошибкой из-за нехватки библиотек.

Поэтому предлагаем устанавливать все вручную.

Подключимся к контейнеру

```shell script
docker exec -it php bash
```

Затем вводим такие комманды:

```shell script
apt-get update && apt-get install -y git curl zip vim unzip
docker-php-ext-install pdo
docker-php-ext-install mysqli
docker-php-ext-install pdo_mysql
docker-php-ext-enable pdo
docker-php-ext-enable mysqli
docker-php-ext-enable pdo_mysql
```

После этого нужно будет выйти из контейнера

```shell script
exit
```

Или нажав

```
Ctrl + C
```

Раскомментировать необходимые расширения в файле **php.ini** в каталоге **./php/**. Например:

```
;extension=mbstring.so
extension=mysqli.so
extension=pdo_mysql.so
```

И перезагрузить контейнеры

```shell script
docker restart php
docker restart nginx
```

Посмотреть версию php:

```shell script
php -v
```

Посмотреть расширения php:

```shell script
php -m
```

[^ к оглавлению](#оглавление)

## Настройка phpMyAdmin

Переменная среды

```
PMA_ARBITRARY=1
```

обозначает, что можно подключаться к любому серверу сети, а не только localhost.

```
UPLOAD_LIMIT=1024M
MEMORY_LIMIT=1024M
MAX_EXECUTION_TIME=300
```

Этими переменными задается максимальный размер бэкапа, который можно загрузить через phpMyAdmin.

phpMyAdmin запускается в отдельном контейнере с Apache2 на 80 порту, но у нас 80 порт уже занят контейнером с веб-сервером Nginx, который на 80 порту публикует статику PHP.

Поэтому мы перебрасываем 80 порт на 8000.

[^ к оглавлению](#оглавление)

## Настройка MySQL

Мы подключаем дамп базы в контейнер, чтобы наша база не удалялась каждый раз когда мы делаем build или чистим проект.

Настройку базы можно производить в phpMyAdmin или через консоль.

Имя сервера mysql указано в файле **.env**

```
MYSQL_HOST=mysql
```

Пользователь с правами администратора всегда:

```
root
```

Там же, в файле **.env**, задан пароль для root

```
MYSQL_ROOT_PASSWORD=1234
```

Также в этом файле прописаны настройки рабочей базы:

```
MYSQL_DB=test
MYSQL_USER=user
MYSQL_PASSWORD=1234
```

Поменяйте их на те, которые будут использоваться в вашем проекте. И затем вам нужно создать базу и пользователя.

Для работы в консоли вам подойдет следующая инструкция.

> Обратите внимание, что вместо переменных окружения вам нужно будет поставить их значения. Например, вместо

```
CREATE DATABASE `_MYSQL_DB_`;
# нужно написать
CREATE DATABASE `test`;
# или имя вашей базы
```

> И не забывайте ставить знак ";" в конце операции!

Подключимся к контейнеру

```
docker exec -it mysql sh
```

Для подключения к самой MySQL внутри контейнера наберем команду

```
mysql -uroot -p
```

Система попросит ввести пароль, вводим пароль из _MYSQL_ROOT_PASSWORD_.

Создадим базу данных

```
CREATE DATABASE `_MYSQL_DB_`;
```

Посмотрим на все базы данных и убедимся, что она создана

```
SHOW DATABASES;
```

Создадим пользователя

```
CREATE USER '_MYSQL_USER_'@'%' IDENTIFIED BY '_MYSQL_PASSWORD_';
```

% обозначает что пользователь может подключаться из под любого хоста. Это важно т.к. разные контейнеры расположены на разных хостах и у них разные ip.

Добавим пользователю все права на базу созданную ранее

```
GRANT ALL PRIVILEGES ON `_MYSQL_DB_` . * TO '_MYSQL_USER_'@'%';
```

Для того чтобы удалить пользователя, нужно будет сначала убрать права, а потом удалить.

```
REVOKE ALL PRIVILEGES, GRANT OPTION FROM '_MYSQL_USER_'@'%';
DROP USER '_MYSQL_USER_'@'%';
```

[^ к оглавлению](#оглавление)

## Дамп MySQL

**Вариант 1** 

Если требуется создать дополнительных пользователей, то следует это сделать перед началом процедуры загрузки дампа.  

В файле **mysql/conf.d/config-file.cnf** отключите лог медленных запросов **slow_query_log=0** или установите большое значение **long_query_time**, например 1000.

Если дамп сжат утилитой gzip, сначала следует распаковать архив:

```shell script
gunzip databases-dump.sql.gz
```

Затем можно развернуть дамп, выполнив на локальном компьютере команду:

```shell script
docker exec -i mysql mysql --user=root --password=secret --force < databases-dump.sql
```

Указывать пароль в командной строке — плохая практика, не делайте так в производственной среде. 

MySQL выдаст справедливое предупреждение:

````
>mysql: [Warning] Using a password on the command line interface can be insecure.
````

Ключ *--force* говорит MySQL, что ошибки следует проигнорировать и продолжить развёртывание дампа. Этот ключ иногда может пригодится, но лучше его без необходимости не применять. 

**Вариант 2**

Воспользоваться утилитой Percona **XtraBackup**. 

Percona **XtraBackup** — это утилита для горячего резервного копирования баз данных MySQL.

О том, как работать с **XtraBackup** можно узнать по ссылке: https://habr.com/ru/post/520458/. 

[^ к оглавлению](#оглавление)

## Дамп PostgreSQL

Выполните следующую команду на локальной машине:

```shell script
docker exec -i postgres psql --username user_name database_name < /path/to/dump/pgsql-backup.sql 
```

или зайдите в контейнер postgres и выполните:

```shell script
psql --username user_name database_name < /path/to/dump/pgsql-backup.sql 
```

**user_name** — имя пользователя. Значение *POSTGRES_USER*.

**database_name** — название базы данных. Значение *POSTGRES_DB*.

[^ к оглавлению](#оглавление)

## Дамп MongoDB

1. Скопируйте фалы дампа в каталог _**mongo/dump**_.

2. Войдите в контейнер mongo:

```shell script
docker exec -it mongo sh
```

Выполните следующую команду, чтобы развернуть дамп базы _**database_name**_:
 
```shell script
mongorestore -d database_name /dump/databases/database_name
```

[^ к оглавлению](#оглавление)

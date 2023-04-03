# Почтовый сервер Mailcow

[Оригинал статьи](https://blog.unixhost.pro/ru/2022/10/mailcow-nastraivaem-sobstvennyj-pochtovyj-server/)

[Видеоинструкция](https://www.youtube.com/watch?v=XESmijy1GvM)

Mailcow — это почтовый сервер который разворачивается в **docker** контейнере и требует минимум настройки. Maicow состоит из Dovecot, ClamAV, Solr, Oletools, Memcached, Redis, MariaDB, Unbound, PHP, Postfix, ACME, Nginx, Rspamd, SOGo, Netfilter.

В этом репозитории нет файлов для **Mailcow**, потому что вся установка и настройка происходит из официального репозитория.

Подробнее см. соответствующий раздел.

# Установка

Устанавливать mailcow необходимо от пользователя root. Подключаемся к серверу под root пользователем, либо выполняем следующую команду

```
sudo su
```

Для установки нам дополнительно потребуется пакет docker-compose-plugin

```
apt install docker-compose-plugin
```

Переходим в папку opt и клонируем репозиторий mailcow и переходим в папку mailcow-dockerized

```
cd /opt
git clone https://github.com/mailcow/mailcow-dockerized
cd mailcow-dockerized
```

Запускаем генерацию файла конфигурации

```
./generate_config.sh
```

Во время генерации конфигурационного файла у нас будет запрошено доменное имя на котором будет находится система mailcow, советуем вам создать на вашем домене поддомен для почты и указать его. Mailcow просит указать имя домена в формате FQDN, а это значит, что точка на конце обязательна. Например

```
mail.example.com.
```

Также потребуется указать часовую зону в формате

```
Europe/Moscow
```

Если на вашем сервере памяти меньше чем 2.5GB скрипт предложит вам отключить ClamAV

Сгенерированный файл конфигурации находится в файле mailcow.conf. При необходимости вы можете его отредактировать.

Для установки выполняем следующие команды

```
docker compose pull
docker compose up -d
```

После установки переходим в админ панель которая находится по адресу https://mail.example.com, либо если вы меняли порт в файле конфигурации то добавляем его в конце доменного имени.

Стандартный логин **admin**, пароль **moohoo**. После первого входа в обязательном порядке меняем пароль у пользователя admin.

Для добавления нового почтового домена, переходим в в раздел Configuration — Mail Setup и нажимаем на зеленую кнопку + Add Domain

Указываем доменное имя, по желанию добавляем описание и тэг для почты. При добавлении нового доменного имени обязательно нужно перегружать контейнер SOGo, для этого предусмотрена отдельная кнопка **Add domain and restart SOGo**, нажимаем ее.

Для создания почтовых ящиков, переходим во вкладку Mailboxes и создаем почтовый ящик нажав на кнопку **Add mailbox**.

После добавления почтового адреса перейдем в webmail и отправим наше первое письмо. Для входа в Webmail вверху нажимаем на App и выбираем Webmail.

Вводим логин, пароль и попадаем в почтовый веб-интерфейс.

# Уточнение

Mailcow устанавливается с поддержкой ipv6 и для того чтобы ее отключить, необходимо отредактировать файл docker-compose.yml. В данном файле находим строку enable_ipv6 и меняем значение на false:

```
networks:
  mailcow-network:
    ...
    enable_ipv6: false
```

# DNS записи

Для работы Mailcow вам необходимо добавить следующие DNS записи для вашего домена

```
# Name              Type       Value
mail                IN A       1.2.3.4
autodiscover        IN CNAME   mail.example.com. (your ${MAILCOW_HOSTNAME})
autoconfig          IN CNAME   mail.example.com. (your ${MAILCOW_HOSTNAME})
@                   IN MX 10   mail.example.com. (your ${MAILCOW_HOSTNAME})
```

Так же необходимо добавить SPF запись указав в ней IP вашего сервера

```
@                   IN TXT     "v=spf1 mx a SERVER_IP -all"
```

И указать DKIM запись которая доступна в панели управления Mailcow в разделе Configuration — Configuration & Details — ARC/DKIM keys

```
dkim._domainkey     IN TXT     "v=DKIM1; k=rsa; t=s; s=email; p=..."
```

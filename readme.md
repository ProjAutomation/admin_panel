# Админка проекта Project Automation

## Установка и запуск
Этот раздел актуален и для локальной разработки и для деплоя.

Склонируйте репозиторий и запустите установку через [Poetry](https://python-poetry.org):

```sh
poetry install
```

Создайте файл `.env` со следующими параметрами:

```ini
DEBUG=False # True для локальной разработки
SECRET_KEY='...'
ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1,... # добавьте ваш домен или IP
```

- `DEBUG=True` включает режим отладки: Django будет выводить подробные сообщения об ошибках прямо в браузере. Критически важно [при деплое указать](https://docs.djangoproject.com/en/4.2/ref/settings/#std:setting-DEBUG) `DEBUG=False`. По умолчанию установлен в `False.`
- `SECRET_KEY` - уникальный набор символов, используется при генерации кук, токенов и пр. важных для безопасности сущностей. Сгенерировать `SECRET_KEY` [можно так](https://stackoverflow.com/a/57678930). Указать нужно обязательно, без него сайт не запустится.
- `ALLOWED_HOSTS` - хосты (домены или IP), которые может обслуживать данный сайт. Указание конкретных разрешённых хостов важно для предотвращения некоторых видов атак. Параметр обязателен для заполнения для обслуживания любых клиентов, отличных от `localhost`.

Запустите миграции:

```sh
poetry run python manage.py migrate
```

Создайте главного администратора:

```sh
poetry run python manage.py createsuperuser
```

## Запуск для разработки
Запустите встроенный Джанго-сервер:

```sh
poetry run python manage.py runserver
```

## Запуск на сервере
На сервере сайт работает на [Gunicorn](https://gunicorn.org) с реверс-прокси через Nginx.

Рекомендуемый порядок действий после выполнения команд из раздела «Установка и запуск»:

```sh
# собрать статику
poetry run python manage.py collectstatic

# узнать путь к Python-окружению проекта (Executable в выводе)
poetry env info
# ...
# Executable: /home/USERNAME/.../bin/python
# ...
```

Запустить Django-приложение через Gunicorn следующей командой, которую для удобства мы сохраним в файле `start.sh` в директории проекта:

```sh
#!/usr/bin/env bash
/home/USERNAME/.../bin/python \
    -m gunicorn -w 3 \
    --chdir /var/www/projects/admin_panel \
    -b localhost:5551 \
    config.wsgi:application
```

Используем `start.sh` в [юните](https://dvmn.org/encyclopedia/deploy/systemd/) для `systemd`:

```ini
; /etc/systemd/system/project_automation_admin.service
[Unit]
Description=Project Automation Admin Panel

[Service]
Type=simple
WorkingDirectory=/var/www/projects/admin_panel
ExecStart=/var/www/projects/admin_panel/start.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

За [отдачу статики и загружаемых фотографий](https://dvmn.org/encyclopedia/web-server/deploy-django-nginx-gunicorn/) на сервере отвечает Nginx.

Пример конфига, где Django-приложение запускается на `localhost:5551` с Nginx в качестве реверс-прокси на `http://<YOUR-ADDRESS>`:

```nginx
server {
  listen <YOUR-ADDRESS>:80;

  location /media/ {
    alias /path/to/admin_panel/media/;
  }

  location = /favicon.ico { access_log off; log_not_found off; }

  location /static/ {
    alias /path/to/admin_panel/staticfiles/;
  }

  location / {
    include '/etc/nginx/proxy_params';
    proxy_pass http://localhost:5552/;
  }
}
```

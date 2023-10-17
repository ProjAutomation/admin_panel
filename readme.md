# Админка проекта Project Automation

## Установка и запуск
Установка через [Poetry](https://python-poetry.org). Склонируйте репозиторий и запустите установку. Poetry сама создать окружение:

```sh
poetry install
```

Далее, накатите миграции:

```sh
make migrate
# или
poetry run python manage.py migrate
```

и запустите сервер:

```sh
make run
# или
poetry run python manage.py runserver
```

## Deploy
Создать `.env`:

```ini
DEBUG=False
SECRET_KEY='...'
ALLOWED_HOSTS=localhost,0.0.0.0,127.0.0.1,...
```

Запустить миграции:

```sh
make migrate
```

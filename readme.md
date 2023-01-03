# Приложение для учета трат пользователей

## Документация
Описание и схема БД находятся в `docs`

## Старт проекта

Создать `.env` файл с `.env.example` ключами из директории `config` и заполнить их необходимыми значениями.

Установить зависимости:
```shell
poetry install
```

Активировать виртуальное окружения:
```shell
poetry shell
```

Накатить миграции:
```shell
python manage.py migrate
```

Создать суперпользователя для доступа к админке:
```shell
python manage.py createsuperuser
```

Запуск приложения:
```shell
python manage.py runserver
```
## Запуск тестов
Run test and quality suits to make sure all dependencies are satisfied and applications works correctly before making changes.
```shell
pytest
```
## Панель администратора
`http://localhost:8000/admin/`

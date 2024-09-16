# API для Управления Подписками Пользователей

В данном репозитории представлен проект, реализующий функциональность блога с возможностью создания постов, комментариев
и подписок на пользователей и группы.
## Стек технологий

![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-FF3C2A?logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?logo=json-web-tokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-009639?logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?logo=gunicorn&logoColor=white)
## Установка

1. Склонируйте данный репозиторий на свой локальный компьютер:

```bash
git clone git@github.com:vivat-7on/api_final_yatube.git
```

2. Перейдите в папку с проектом:

```bash
cd api_final_yatube
```

3. Установите необходимые зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

Для запуска проекта выполните следующую команду:

```bash
python manage.py runserver
```

Проект будет доступен по адресу http://localhost:8000/

## API Endpoints

Проект предоставляет следующие API endpoints:

- `/api/v1/posts/` - CRUD API для работы с постами.
- `/api/v1/groups/` - API для просмотра списка групп.
- `/api/v1/posts/<post_id>/comments/` - CRUD API для работы с комментариями к посту.
- `/api/v1/follow/` - CRUD API для работы с подписками на пользователей.

### Аутентификация

Для доступа к некоторым API endpoints требуется аутентификация. В нашем проекте используется аутентификация с помощью
токенов. Для получения токена необходимо выполнить запрос на `/api/v1/jwt/create/`, предоставив логин и пароль
пользователя.

Пример запроса на получение токена:

```bash
curl -X POST -d "username=ваш-логин&password=ваш-пароль" http://localhost:8000/api/v1/jwt/create/
```

В ответ на этот запрос вы получите токен, который нужно использовать в заголовке запросов для доступа к защищенным API
endpoints.

Пример использования токена в заголовке:

```bash
curl -H "Authorization: Bearer ваш-токен" http://localhost:8000/api/v1/защищенный-ресурс/
```


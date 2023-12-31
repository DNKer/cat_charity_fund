# ฅ^•ﻌ•^ฅ QRkot *ฅ^•ﻌ•^ฅ*

## Описание 🐾

Приложение для Благотворительного фонда поддержки котиков.

**QRkot** - это API сервиса по сбору средств для финансирования благотворительных проектов. Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.

## Особенности

- Сразу после создания нового проекта или пожертвования запускается процесс «инвестирования» (увеличение внесенной суммы как в пожертвованиях, так и в проектах)  🐾.
- После того как необходимая сумма набирается, проект закрывается.
- Настроено автоматическое создание первого суперпользователя при запуске проекта.
- Возможность регистрации пользователей, добавления благотворительных проектов и пожертвований, которые распределяются по открытым проектам.Если создан новый проект, а в базе были «свободные» (не распределённые по проектам) суммы пожертвований — они автоматически инвестируются в новый проект. То же касается и создания пожертвований: если в момент пожертвования есть открытые проекты, эти пожертвования  автоматически🐾зачисляются на их счета.

<img src="tests\fixtures\logo_cats.png" alt="drawing" width="300" align="center"/>

## Технологии

[![Python 3.9](https://img.shields.io/badge/Python-3.9-464646?style=plastic&color=008080)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=plastic&logo=FastAPI&logoColor=56C0C0&color=008080)](https://fastapi.tiangolo.com/)
[![asyncio](https://img.shields.io/badge/-asyncio-464646?style=plastic&color=008080)](https://docs.python.org/3.9/library/asyncio.html)
[![pyJWT](https://img.shields.io/badge/-pyJWT-464646?style=plastic&color=008080)](https://pypi.org/project/PyJWT/)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4.36-blue)
![Alembic](https://img.shields.io/badge/Alembic-1.7.7-blue)


## Установка

> приводятся команды для `Windows`.

Клонировать репозитарий:

```bash
git clone git@github.com:DNKer/cat_charity_fund.git
```

Cоздать и активировать виртуальное окружение:

```bash
python -m venv venv
```

```bash
source venv/scripts/activate
```

Обновить систему управления пакетами:

```bash
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```bash
pip install -r requirements.txt
```

Создать в корневой директории файл .env со следующим содержимым (в репозитории есть [пример](example.env)):

```
APP_TITLE=Заголовок (название приложения)
APP_AUTHOR=Author
DESCRIPTION=Описание
DATABASE_URL=sqlite+aiosqlite:///./<название базы данных>.db
SECRET=<секретное слово>
FIRST_SUPERUSER_EMAIL=<email суперюзера>
FIRST_SUPERUSER_PASSWORD=<пароль суперюзера>
```

Применить миграции для создания базы данных SQLite:
```bash
alembic upgrade head
```
Проект развернут и готов к локальному запуску.

## Управление:
Для локального запуска выполните команду:
```bash
uvicorn app.main:app --reload
```
Сервис будет запущен и доступен по следующим адресам:
- http://127.0.0.1:8000 - API
- http://127.0.0.1:8000/docs - автоматически сгенерированная документация Swagger
- http://127.0.0.1:8000/redoc - автоматически сгенерированная документация ReDoc

Документация также размещена в виде [файла](openapi.json) в корневой директории.

## Права пользователей:
Любой посетитель сайта (в том числе неавторизованный) может посмотреть список всех проектов.
Любой зарегистрированный пользователь может сделать пожертвование.
Зарегистрированный пользователь может просматривать только свои пожертвования. Информация о том, инвестировано пожертвование в какой-то проект или нет, обычному пользователю недоступна.
Суперпользователь может просматривать список всех пожертвований, при этом ему выводятся все поля модели.
Никто не может менять через API размер внесённых средств, удалять или модифицировать закрытые проекты, изменять даты создания и закрытия проектов.

## Примеры работы с API для неавторизованных пользователей.

### &#128221; _Регистрация нового пользователя:_
```http
POST http://127.0.0.1:8000/auth/register
```
```json
{
  "email": "string",
  "username": "string"
}
```
### &#128273; _Получение JWT-токена (аунтификация):_
```http
POST http://127.0.0.1:8000/auth/jwt/login
```
```json
{
  "username": "string",
  "password": "string"
}
```
В ответ придет токкен ```access_token```, который необходимо передавать в заголовке каждого запроса:
```json
{
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiOTIyMWZmYzktNjQwZi00MzcyLTg2ZDMtY2U2NDJjYmE1NjAzIiwiYXVkIjoiZmFzdGFwaS11c2VyczphdXRoIiwiZXhwIjoxNTcxNTA0MTkzfQ.M10bjOe45I5Ncu_uXvOmVV8QxnL-nZfcH96U90JaocI",
"token_type": "bearer"
}
```
### &#128682; _Выход (сброс jwt-токена):_
```http
POST http://127.0.0.1:8000/auth/jwt/logout
```
```json
{
  "username": "string",
  "password": "string"
}
```
### &#128209; _Просмотреть список проектов (может как __авторизованный__, так и  __неавторизованный__ пользователь):_
```http
POST http://127.0.0.1:8000/charity_project/
```
## Примеры работы с API для авторизованных пользователей.
### &#10133; _Создание проекта:_
```http
POST http://127.0.0.1:8000/charity_project/
```
```json
{
"name": "string",
"description": "string",
"full_amount": 0
}
```
### &#128257; _Изменение проекта под номером project_id:_
```http
PATCH http://127.0.0.1:8000/charity_project/{project_id}
```
```json
{
"name": "string",
"description": "string",
"full_amount": 0
}
```
### &#10060; _Удаление проекта под номером project_id:_
```http
DELETE http://127.0.0.1:8000/charity_project/{project_id}
```
### &#128209; _Просмотреть список своих пожертвований (может только __авторизованный__ пользователь):_
```http
GET http://127.0.0.1:8000/donation/my/
```
Зарегистрированный пользователь может просматривать __только свои__ пожертвования, при этом ему выводится только четыре поля: ```id```, ```comment```, ```full_amount```, ```create_date```. Информация о том, инвестировано пожертвование в какой-то проект или нет, обычному пользователю недоступна.

Если пользователю присвоен статус _суперпользователь_, то он может просматривать список всех пожертвований, при этом ему выводятся все поля.
### &#128209; _Просмотреть список пожертвований (может только __суперпользователь__):_
```http
GET http://127.0.0.1:8000/donation/
```
### &#10133; _Создание пожертвования:_
```http
POST http://127.0.0.1:8000/donation/
```
```json
{
"full_amount": 0,
"comment": "string"
}
```

Никто не может менять через API размер внесённых средств, удалять или модифицировать закрытые проекты, изменять даты создания и закрытия проектов.

## Примеры работы c пользователями.

### &#128209; _Получение данных о пользователе по id (может только __суперпользователь__):_ ###

```http
GET http://127.0.0.1:8000/users/{id}/
```

### &#128209; _Получение данных о себе (может только __авторизованный__ пользователь):_  ###
```http
GET http://127.0.0.1:8000/users/me/
```


#### Лицензия <img src="tests\fixtures\qr.PNG" width="148" height="148" title="QR код" align="right"/>
###### Free Software, as Is 
###### _License Free_
###### Author: [Dmitry](https://github.com/DNKer), [Yandex practikum](https://practicum.yandex.ru)
###### 2023
# REST API ресторана
# !!! В ЭТОМ РЕПОЗИТОРИИ РЕАЛИЗОВАНА ИНТЕГРАЦИЯ С GOOGLE SHEETS !!!
### ИНСТРУКЦИИ ПО ЗАПУСКУ В РАЗДЕЛЕ "Запуск приложения в контейнерах"
### README ДОПОЛНЕН НОВОЙ ИНФОРМАЦИЕЙ

<h3 align="left">Технологии:</h3>
<div align="center">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="40" alt="python logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg" height="40" alt="fastapi logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg" height="40" alt="postgresql logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sqlalchemy/sqlalchemy-original.svg" height="40" alt="sqlalchemy logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg" height="40" alt="redis logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/pytest/pytest-original.svg" height="40" alt="pytest logo"  />
  <img width="12" />
  <img src="https://www.vectorlogo.zone/logos/rabbitmq/rabbitmq-icon.svg" alt="rabbitMQ" width="40" height="40"/>
  <img width="12" />
  <img src="https://cdn.simpleicons.org/docker/2496ED" height="40" alt="docker logo"  />
  <img width="12" />
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg" height="40" alt="git logo"  />
  <img width="12" />
  <img src="https://skillicons.dev/icons?i=github" height="40" alt="github logo"  />
</div>

## Разделы
- [Технические задания](#технические-задания)
- [Описание API](#описание-api)
    - [Файл администратора](#excel-файл-администратора)
		- [Добавлен URL-параметр id](#добавлен-post-query-string-параметр-id)
	- [Endpoint `getall/`](#endpoint-getall)
    - [Запуск приложения в контейнерах](#запуск-приложения-в-контейнерах)
		- [Стандартный запуск](#стандартный-запуск)
        - [Запуск тестов](#запуск-асинхронных-тестов-на-pytest-с-помощью-docker-compose)
		- [(!!!)Запуск в режиме синхронизации с Google sheets](#запуск-в-режиме-синхронизации-с-google-sheets)
    - [Кэширование Redis](#кэширование)
    - [Паттерны Репозиторий и Сервисный слой](#паттерны)
    - [Тестирование](#тестирование)
        - [Структура БД для тестирования](#структура-бд-используемая-для-тестирования)
- [Pre-commit hooks](#pre-commit-checks)
- [Запуск приложения вручную (не актуально)](#запуск-приложения-вручную-не-актуально)
- [Результаты тестирования Postman](#резльтаты-тестирования-postman)

<br>
<br>

## Технические задания
1. <a href="assignment/Homework_1.md"> <b>Требования к разрабатываемому API ресторана</b> </a>

2. <a href="assignment/Homework_2.md"> <b>Требования к интеграционному тестировнию API ресторана</b> </a>

3. <a href="assignment/Homework_3.md"> <b>Разграничение бизнес логики с помощью паттернов (например, MVC, Репозиторий, Сервисный слой и др.). Кэширование на Redis. Аннотации типов и проверка с помощью pre-commit hooks</b> </a>

4. <a href="assignment/Homework_4.md"> <b>Асинхронная работа и бэкграунд таски с помощью BackgroundTasks и Celery, синхронизация с excel файлом</b> </a>
<br>

## Описание API
CRUD REST API ресторана, содержащий следующие сущности:
- Меню/ Menue
- Подменю/ Submenu
- Блюдо/ Dish

Реализована возможность создавать, читать, обновлять и удалять эти сущности. Добавлен эндпоинт `http://localhost:8000/getall/`, позволяющий получить одним запросом все меню, связанные соответственно подменю и блюда в виде JSON-"матрешки". Предусмотрено кэширование с точечной инвалидацией. Инвалидация происходит через BackgroundTasks. Приложение и все СУБД контейнеризированы. Запуск с помощью команды `docker-compose up -d`. **API, базы данных и тесты полностью асинхронные.**
Файл [.env.example](/.env.example) используется для хранения переменных окружения, необходимых для подключения к БД внутри Docker контейнера. *Убрал из .gitignore упоминание `.env` из соображений удобства проверки преподавателем.*

- **Код проекта соответствует принципам SOLID, DRY и KISS.**
- **Проект  запускается по одной команде Docker compose**
- **Успешно выполняются все тесты Postman при изначально пустой БД**
- **Успешно выполняются все асинхронный тесты на Pytest. Запуск тестов по одной команде Docker compose**
- **Реализован вывод количества подменю и блюд для Меню через один ORM запрос**
- **[Реализован тестовый сценарий](tests/test_quantity.py), аналогичный сценарию «Проверка кол-ва блюд и подменю в меню» из Postman с помощью Pytest**
- **Проект покрыт тайпхинтами и проходят все pre-commit хуки**
- **Подготовлена [документация](/openapi.json) в соответствии с OpenAPI**
- **Реализована односторонняя синхронизация базы данных из файла [google sheets](https://docs.google.com/spreadsheets/d/1HhPN8TKMyfb8Yy5dZ5S_reSsGHxike4Tv4P8VSz28o8/edit#gid=0). Данные из google sheets запрашиваются через Google API, парсятся, на их основе формируется датафрейм из которого в Volume контейнера в папке admin создается актуальный файл Menu.xlsx, с которым уже ведется работа по синхронизации с БД. В данном случае bind mount не используется.**



## Excel файл администратора
Для комфортного использования приложения разработана система односторонней синхронизации Excel файла [Menu.xlsx](admin/Menu.xlsx) в папке [/admin](/admin) с базой данных по API каждые 15 секунд в рамках фоновой задачи, запускаемой в Celery.

> **Important**
> **Файл [Menu.xlsx](admin/Menu.xlsx) связан с контейнером напрямую через [Bind mount](https://docs.docker.com/storage/bind-mounts/) и поэтому доступен администратору для редактирования через файловую систему пользовательского компьютера.**
<div align='center'>
<img src='https://docs.docker.com/storage/images/types-of-mounts-bind.png'>
</div>


Изменения, которые необходимо отразить в БД, определяются относительно файла `.previous_state_menu.xlsx`, который хранится уже непосредственно в Volume контейнера Celery и не виден пользователю из файловой системы. После внесения изменений в БД в этот файл сохраняет текущее состояние администраторского Excel файла, после чего используется для сравнения с ним и определения изменений. Все изменения вносятся асинхронными запросами к API с помощью библиотеки [aiohttp](https://docs.aiohttp.org/en/stable/client_quickstart.html). Парсинг Excel файла осуществляется с помощью библиотеки [Pandas](https://pandas.pydata.org/).

> **Note**
> Резонное ограничение на уникальность (ID) ключей экземпляров сущностей в базе данных требует, чтобы ID в Excel таблице тоже были уникальными в рамках одной сущности (!).

#### Добавлен POST query string параметр `id`
Для первоначального заполнения таблицы и последующего добавления элементов из Excel файла (который содержит заданные пользователм id) был доработан существующий POST эндпоинт: добавлена поддержка [Query String](https://en.wikipedia.org/wiki/Query_string) с опциональным параметром *id* (например `POST http://127.0.0.1:8000/menus/?id=123`), что позволяет передавать созданный пользователем ID в базу данных. В случае, если параметр не будет передан в URL, то в качестве первичного ключа будет сгенерирован UUID.

## Endpoint `getall/`
Возвращает все меню, связанные с ними подменю и связанные с ними блюда одним запросом.

#### Структура JSON ответа эндпоинта:

<img src='docs\JSON-getall3.png'>



## Запуск приложения в контейнерах

|      |   Образы для Docker      |
|------|--------------------------|
|API   | python:3.10-slim         |
|DB    | postgres:15.1-alpine     |
|Cache | redis/redis-stack:latest |
|Celery| python:3.10-slim         |
|Broker| RabbitMQ                 |


### Стандартный запуск:

```
docker-compose up -d
```
API будет доступен по следующему URL: http://127.0.0.1:8000/api/v1/

> **Important**
> Тесты на Postman  следует запускать на пустой БД, поэтому следует очистить [Excel](admin/Menu.xlsx) таблицу администратора и подождать ~15 секунд, чтобы база данных пришла в соответствие.
<br><br>

### Запуск асинхронных тестов на Pytest с помощью Docker-compose:

```
docker-compose -f docker-compose-tests.yml up
```
Результаты тестирования будут выведены в терминал.
Добавлен 34-ый тест на эндпоинт, возвращающий все сущности: `http://localhost:8000/api/v1/getall/`.
<br><br>


### Запуск в режиме синхронизации с Google sheets:

```
docker-compose -f docker-compose-google.yml up
```

Файл доступен по ссылке:
https://docs.google.com/spreadsheets/d/1HhPN8TKMyfb8Yy5dZ5S_reSsGHxike4Tv4P8VSz28o8/edit?usp=sharing

## Кэширование
Для хранения кэша использована NoSQL база данных [Redis](https://redis.io/).

**_Реализована точечная инвалидация кэша._
В качестве ключей в Reids используется URL ресурса, с помощью фильтрации по которому происходит точечная инвалидация всех зависимых объектов в кэшэ.** *Время хранения каждой записи в кэшэ принято 60 секунд.*


## Паттерны
<div align='center'>
<img src="docs/RepositoryPattern.png" alt="postman test results 100%" alt="Centered Image" height='400'>
</div>

В проекте реализованы паттерны Репозиторий и Сервисный слой, что позволяет изолировать и передать работу с базами данных (SQL-ORM и NoSQL) соответствующим [репозиториям](app/repositories/), а всю подготовку данных к передаче в эндпоинты берет на себя [Сервисный слой](app/services/).


## Тестирование

Для интеграционного тестирования работы API использована библиотека [Pytest](https://docs.pytest.org/).

Реализованы 34 **асинхронных** интеграционных CRUD теста для всех эндпоинтов. Проверка Read, Update, Delete методов реализована с помощью фикстур, расположенных в файле [conftest.py](tests/conftest.py), которые создают модели тестируемых ресурсов напрямую в тестовой БД.

Реализован [тестовый сценарий](tests/test_quantity.py), проверяющий правильность подсчета:
- количества подменю и блюд относящихся к определенному основному меню;
- количества блюд относящихся к определенному подменю.

## Структура БД, используемая для тестирования
```
Restaurant
├── Menu 1
│   ├── Submenu 1
│   │   ├── Dish 1
│   │   └── Dish 2
│   └── Submenu 2
│       └── Dish 3
├── Menu 2
│   └── Submenu 3
└── Menu 3
```
[link to this ASCII Tree generator](https://tree.nathanfriend.io/?s=(%27options!(%27fancy!true~fullPath5~trailingSlash5~rootDot5)~6(%276%27Restaurant-M41.10102.203-M42.3-%27)~version!%271%27)*%20%20-%5Cn*.-*Subm40-**Dish%204enu%205!false6source!%016540.-*)
<br>БД заполняется фикстурами и проверяется правильность значений, передаваемых в полях `submenu_count` и `dish_count` в JSON-ответах на GET запросы к различным меню и подменю. <br> <br>


### Pre-commit checks
В проекте везде использовались тайпхинты с последующей проверкой [MyPy](https://github.com/python/mypy).
Полный список всех чеков представлен ниже:

<img src="docs/pre-commit-hooks-results.png" alt="postman test results 100%">
<br>
<br>
<br>
<br>
<br>




> ## Запуск приложения вручную (не актуально)

> Для разработки использовался Python3.11

> 1. Рекомендуется развернуть виртуальное окружение и установить в него все зависимости.

> ```console
> python3 -m venv venv
> source venv/bin/activate # на Linux
> pip install -r requirements.txt
> ```

> 2. В файле переменных окружения [.env](/.env.example) убедится, что в качестве хостов баз данных укзан localhost
> исправить на localhost
> ```
> DATABASE_HOSTNAME=127.0.0.1
> REDIS_HOST=127.0.0.1
> ```

> 3. Установить Docker самостоятельно. Затем требуется скачать образы Postgres:Alpine и redis-stack:latest, а затем запустить контейнер. Это можно сделать с помощью следущих Docker команд.
> ```console
> docker run --name pg-restaurant -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=data -e TZ=Europe/Moscow --restart=always -d postgres:15.1-alpine;
> docker start pg-restaurant;
> docker run -p 6379:6379 -it redis/redis-stack:latest
> ```
> Порт контейнера Postgres 5432 прокидывается на порт машины 5432.
> Порт контейнера с Redis 6379 прокоидвается на 6379.

> 4. Для запуска приложения рекомендуется использовать ASGI веб сервер [uvicorn](https://www.uvicorn.org/).
> ```console
> uvicorn app.main:app
> ```
> <br>

## Результаты тестирования Postman
<img src="docs/postman_test_results.png" alt="postman test results 100%">



<!--- quickly update both repositories in one command ---!>
<!--- git add .; git commit -m 'Update README.md'; git push origin main; git checkout homework-4; git pull origin main; git push origin homework-4; git checkout main; ---!>

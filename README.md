## Разделы
- [Технические задания](#технические-задания)
- [Описание API](#описание-api)
- [Тестирование](#тестирование)
- [Запуск приложения в контейнерах](#запуск-приложения-в-контейнерах)
- [Запуск приложения вручную](#запуск-приложения-вручную)
- [Результаты тестирование в Postman](#результаты-тестирование-в-Postman)


### Технические задания
1. <a href="assignment/Homework_1.md"> <b>Требования к разрабатываемому API ресторана</b> </a>

2. <a href="assignment/Homework_2.md"> <b>Требования к интеграционному тестировнию API ресторана</b> </a>

3. <a href="assignment/Homework_3.md"> <b>Разграничение бизнес логики с помощью паттернов (например, MVC, Репозиторий, Сервисный слой и др.). Кэширование на Redis. Аннотации типов и проверка с помощью pre-commit hooks</b> </a>
<br>
## Описание API
CRUD REST API ресторана, содержащий слеудующие сущности:
- Меню/ Menue
- Подменю/ Submenu
- Блюдо/ Dish

Реализована возможность создавать, считывать, обновлять и удалять эти сущности. Настроено взаимодействие с СУБД PostgreSQL в Docker контейнере. В окружение контейнера прокинуты московская таймзона и необходимые для создания базы данных переменные. Файл [.env](/.env) используется для хранения переменных окружения, необходимых для подключения к БД внутри Docker контейнера. Убрал из .gitignore упоминание `.env` из соображений удобства проверки преподавателем.
<br><br>

### Кэширование
Для хранения кэша использована NoSQL база данных [Redis](https://redis.io/). Принимается, что запись новых меню, подменю и блюд будет существенно реже, чем их чтение, поэтому весь кэш инвалидируется при любых Create, Update, Delete операциях. Время хранения каждой записи в кэшэ принято 60 секунд.

### Паттерны
<img src="docs/RepositoryPattern.png" alt="postman test results 100%" alt="Centered Image" align="middle">

В проекте реализованы паттерны Репозиторий и Сервисный слой, что позволяет полностью передать работу с базами данных (SQL-ORM и NoSQL) соотвутствующим [репозиториям](app/repositories/), а всю подготовку данных к передаче в функции эндпоинтов берет на себя [Сервисный слой](app/services/).


### Тестирование

Для интеграционного тестирования работы API использована библиотека [Pytest](https://docs.pytest.org/).

Реализовны 33 синхронных CRUD теста для всех эндпоинтов. Проверка Read, Update, Delete методов реализована с помощью фикстур, расположенных в файле [conftest.py](tests/conftest.py), которые создают модели тестируемых ресурсов напрямую в тестовой БД.

Реализован [тестовый сценарий](tests/test_quantity.py), проверяющий правильность подсчета:
- количества подменю и блюд относящихся к определенному основному меню;
- количества блюд относящихся к определенному подменю.

#### Структура БД, используемая для тестирования
```
Restaurant
├── Menu 1
│   ├── Submenu 1
│   │   ├── Dish 1
│   │   └── Dish 2
│   └── Submenu 2
│       └── Dish 3
└── Menu 2
    └── Submenu 3
```
[link to this ASCII Tree generator](https://tree.nathanfriend.io/?s=(%27options!(%27fancy!true~fullPath5~trailingSlash5~rootDot5)~6(%276%27Restaurant-M41.10102.203-M42.3-%27)~version!%271%27)*%20%20-%5Cn*.-*Subm40-**Dish%204enu%205!false6source!%016540.-*)
<br><br>


### Pre-commit checks
В проекте везде использовались тайпхинтинги с последующей проверкой [MyPy](https://github.com/python/mypy).
Полный список всех чеков представлен ниже:

<img src="docs/pre-commit-hooks-results.png" alt="postman test results 100%">


## Запуск приложения в контейнерах

|     |   Образы для Docker      |
|-----|--------------------------|
|API  | python:3.10-slim         |
|DB   | postgres:15.1-alpine     |
|Cache| redis/redis-stack:latest |


### 1. Запуск приложения с помощью Docker-compose

```
docker-compose up -d
```
API будет доступен по адресу: http://127.0.0.1:8000/api/v1/
<br><br>

### 2. Запуск тестов и баз данных для тестирования с помощью Docker-compose
```
docker-compose -f docker-compose-tests.yml up
```
Результаты тестирования будут выведены в терминал.
<br><br>

## Запуск приложения вручную

Для разработки использовался Python3.11

1. Рекомендуется развернуть виртуальное окружение и установить в него все зависимости.

```console
python3 -m venv venv
source venv/bin/activate # на Linux
pip install -r requirements.txt
```

2. В файле переменных окружения [.env](/.env.example) убедится, что в качестве хостов баз данных укзан localhost
исправить на localhost
```
DATABASE_HOSTNAME=127.0.0.1
REDIS_HOST=127.0.0.1
```

3. Установить Docker самостоятельно. Затем требуется скачать образы Postgres:Alpine и redis-stack:latest, а затем запустить контейнер. Это можно сделать с помощью следущих Docker команд.
```console
docker run --name pg-restaurant -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=data -e TZ=Europe/Moscow --restart=always -d postgres:15.1-alpine;
docker start pg-restaurant;
docker run -p 6379:6379 -it redis/redis-stack:latest
```
Порт контейнера Postgres 5432 прокидывается на порт машины 5432.
Порт контейнера с Redis 6379 прокоидвается на 6379.

4. Для запуска приложения рекомендуется использовать ASGI веб сервер [uvicorn](https://www.uvicorn.org/).
```console
uvicorn app.main:app
```
<br><br>
## Результаты тестирование в Postman
<img src="docs/postman_test_results.png" alt="postman test results 100%">

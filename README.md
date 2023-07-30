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

<br><br>
## Описание API
CRUD REST API ресторана, содержащий слеудующие сущности:
- Меню/ Menue
- Подменю/ Submenu
- Блюдо/ Dish

Реализована возможность создавать, считывать, обновлять и удалять эти сущности. Настроено взаимодействие с СУБД PostgreSQL, которую рекомендуется запускать в Docker на основе файла [docker-compose.yml](dcoker-compose.yml). Используется легковесный образ Postgres:Alpine, в окружение контейнера прокинуты московская таймзона и необходимые для создания базы данных переменные. Файл .env используется для хранения переменных окружения, необходимых для подключения к БД. Убрал из .gitignore упоминание .env из соображений удобства проверки преподавателем.  <br>

### Тестирование

Для интеграционного тестирования работы API использована библиотека [Pytest](https://docs.pytest.org/).  

Реализовны 33 синхронных CRUD теста для всех эндпоинтов. Проверка Read, Update, Delete методов реализована с помощью фикстур, расположенных в файле [conftest.py](tests/conftest.py), которые создают модели тестируемых ресурсов напрямую в тестовой БД.  

Реализован [тестовый сценарий](tests/test_quantity.py), проверяющий правильность подсчета:
- количества подменю и блюд относящихся к определенному основному меню;
- количества блюд относящихся к определенному подменю.

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




## Запуск приложения в контейнерах

|     |Образы для Docker     |
|-----|----------------------|
|API  | python:3.10-slim     |
|DB   | postgres:15.1-alpine |   

<br><br>
### 1. Запуск приложения с помощью Docker-compose

```
docker-compose up -d
```
API будет доступен по адресу: http://127.0.0.1:8000/api/v1/
<br><br>

### 2. Запуск тестов и базы для тестирования с помощью Docker-compose
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

2. В файле переменных окружения [.env](/.env) хост с имени контейнера
```
DATABASE_HOSTNAME=db
```
исправить на localhost
```
DATABASE_HOSTNAME=127.0.0.1
```

3. Установить Docker самостоятельно. Затем требуется скачать образ Postgres:Alpine и запустить контейнер. Это можно сделать с помощью следущих Docker команд. 
```console
docker run --name pg-restaurant -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=data -e TZ=Europe/Moscow --restart=always -d postgres:15.1-alpine;
docker start pg-restaurant;
```
Порт базы контейнера 5432 прокидывается на порт машины 5432.

4. Для запуска приложения рекомендуется использовать ASGI веб сервер [uvicorn](https://www.uvicorn.org/).
```console
uvicorn app.main:app 
```
<br><br>
## Результаты тестирование в Postman 
<img src="docs/postman_test_results.png" alt="postman test results 100%">



  

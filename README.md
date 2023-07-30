### Технические задания 
1. <a href="assignment/Homework_1.md"> <b>Требования к разрабатываемому API ресторана</b> </a>

2. <a href="assignment/Homework_2.md"> <b>Требования к интеграционному тестировнию API ресторана</b> </a>


### Описание API
CRUD REST API ресторана, содержащий слеудующие сущности:
- Меню/ Menue
- Подменю/ Submenu
- Блюдо/ Dish

Реализована возможность создавать, считывать, обновлять и удалять эти сущности. Настроено взаимодействие с СУБД PostgreSQL, которую рекомендуется запускать в Docker на основе файла [docker-compose.yml](dcoker-compose.yml). Используется легковесный образ Postgres:Alpine, в окружение контейнера прокинуты московская таймзона и необходимые для создания базы данных переменные. Файл .env используется для хранения переменных окружения, необходимых для подключения к БД. Убрал из .gitignore упоминание .env из соображений удобства проверки преподавателем.  

### Запуск приложения вручную

Для разработки использовался Python3.11  
1. Рекомендуется развернуть виртуальное окружение и установить в него все зависимости.

```console
python3 -m venv venv 
source venv/bin/activate # на Linux
pip install -r requirements.txt
```

2. Установить Docker самостоятельно. Затем требуется скачать образ Postgres:Alpine и запустить контейнер. Это можно сделать с помощью следущих Docker команд. 
```console
docker run --name pg-restaurant -p 5432:5432 -e POSTGRES_PASSWORD=password -e POSTGRES_DB=data -e TZ=Europe/Moscow -d postgres:15.1-alpine;
docker start pg-restaurant;
```
Порт базы контейнера 5432 прокидывается на порт машины 5432.

3. Для запуска приложения рекомендуется использовать ASGI веб сервер [uvicorn](https://www.uvicorn.org/)
```console
uvicorn app.main:app 
```

#### Результаты тестирование в Postman 
<img src="docs/postman_test_results.png" alt="postman test results 100%">



  
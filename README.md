# Тестовое задание для BostonGene
Веб-сервис позволяет  посчитать MD5 хеш от файла 
расположенного в интернете. Расчет хеша и считывание файла
происходят в фоновом режиме. Для локального запуска и 
хранения данных о задаче используется база данных
SQLite3, также сервис можно собрать в Docker, там используется
база данных MySQL.<br>
В базе данных хранится одна сущность **Task**, которая имеет следующие поля:
* **id** - уникальный идентификатор задачи
* **url** - url по которому нужно забрать файл
* **email** - email по которому нужно отправить результат
* **md5** - результат выполнения задачи
* **complete** - статус выполнения задачи

### Основные методы API
Методы обрабатывают HTTP запросы
### Загрузить задачу
Запрос
```bash
curl -X POST -d "url=http://site.com/file.txt&email=example@abc.ru" \
http://localhost:8000/submit
```
Ответ: id созданной задачи или http код ошибки
### Проверить статус выполнения задачи
Запрос
```bash
curl -X GET \
 http://localhost:8000/check?id=0e4fac17-f367-4807-8c28
```
Ответ: статус выполнения задачи, с соотвествующим кодом выполнения. Если
задача выполнена, то url из первого запроса и результат.<br>

Если был указан электронный адрес, то результат придет и туда.

Проект поддерживает сборку в Docker
Сначала нужно установить зависимости (redis, mysql)
```bash
sudo docker run --name redis \
 -d -p 6379:6379 \
 redis:3-alpine
```

```bash
sudo docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \
    -e MYSQL_DATABASE=tc -e MYSQL_USER=tc \
    -e MYSQL_PASSWORD=<DATABASE-PASSWORD> \
    mysql/mysql-server:5.7
```
Далее необходимо собрать проект
```bash
sudo docker build -t tc:latest .
```
После чего запустить HTTP сервер вместе со всеми зависимостями.
```bash
sudo docker run --name tc \
 -d -p 8000:5000 --rm \
 --link mysql:dbserver \
 --link redis:redis-server \
 --env-file ./.env \
 tc:latest
```
И redis-queue
```bash
sudo docker run \
 --name rq-worker \
 -d --rm \
 --link mysql:dbserver \
 --link redis:redis-server \
 --env-file ./.env \
 --entrypoint venv/bin/rq \
 tc:latest \
 worker -u redis://redis-server:6379/0 tc-tasks
```

Для локальной работы без Docker, необходимы python 3.6+, redis-server.
* Клонируем проект
* Создаем виртуальное окружение 
```bash
python -m venv venv
```
* Активируем виртуальное окружение
```bash
source venv/bin/activate
```
* Устанавливаем зависимости из requirements.txt
* Устанавливаем переменные окружения
```bash
export FLASK_APP=application.py
```
* Запускаем http сервер командой flask run, и в другом окне терминала(с включенным виртуальным окружением) redis-queue командой rq worker tc-tasks
* Запускаем команду
```bash
flask db upgrade
```
* Убираем из файла .env параметр DATABASE_URI (чтобы использовалась SQLITE3)

При локальном запуске api доступно на порту 5000, при  запуске из Docker
на порту 8000

Также, для корректной отправки электронной почты необходимо будет отредактировать файл .env
поля MAIL_USERNAME, MAIL_PASSWORD

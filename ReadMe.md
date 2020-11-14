 online-spb-pochta Dragon IT



## Требования

- Установить [Docker](https://www.docker.com/products/docker-desktop)
- `git clone https://gitlab.com/urands/online-hack-rif-2020.git`

## Запуск сервера

Перейти в папку проекта:

```bash
docker-compose build
docker-compose up -d
```

Открываем наше приложение: [http://127.0.0.1](http://127.0.0.1)

Для разработки дополнительно доступен прямой доступ к бекенду и БД

- backend: 127.0.0.1:5000
- db: 127.0.0.1:3306

## Остановка сервера

```bash
docker-compose down
```

### Запуск backend отдельно

```bash
#запустить образ
docker-compose up backend -d
```

### Запуск backend

```bash
#запустить образ
docker-compose down
```

### Запуск frontend

```bash
#запустить фронтенд
запуск из папки  my-app которая находится внутри папки frontend
Как запустить [тут](frontend/my-app/README.md)

### Тестовое API

>   Базовый адрес API: [http://(server)/api/](http://127.0.0.1:/api/)

  + GET [/todos](http://127.0.0.1:/api/todos)  -  Список задач
  + GET [/todos/[id]](http://127.0.0.1:/api/todos/task) - Пролучение одной задачи
  + DELETE /todos/[id]  - Удаление одной задачи
  + POST /todos  - Создание одной задачи params:  task=[task name]
```
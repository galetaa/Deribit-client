# Deribit Client API

Проект представляет собой контейнеризированное FastAPI приложение, которое предоставляет API для работы с данными о ценах, поддерживает мониторинг с использованием Prometheus и Grafana. Данные хранятся в базе данных PostgreSQL, а Docker Compose используется для организации всего окружения. В проекте также реализованы тесты для проверки API.

## Структура проекта

- **`client.py`**: Скрипт для получения данных из внешних источников и их записи в базу данных.
- **`database.py`**: Описание структуры базы данных и подключение к ней.
- **`main.py`**: FastAPI приложение с маршрутами для доступа к данным о ценах.
- **`docker-compose.yml`**: Конфигурация Docker Compose для организации всех сервисов.
- **`prometheus/prometheus.yml`**: Конфигурационный файл для Prometheus.
- **`grafana/`**: Каталог с конфигурацией для Grafana.
- **`tests/`**: Каталог с тестами.
- **`requirements.txt`**: Список зависимостей для проекта.

## Предварительные требования

- **Docker**: Убедитесь, что Docker установлен и работает на вашем компьютере.
- **Docker Compose**: Для управления многоконтейнерными приложениями в Docker.

## Описание сервисов

В `docker-compose.yml` настроены следующие сервисы:

- **db**: База данных PostgreSQL для хранения данных о ценах.
- **client**: Сервис-клиент для загрузки данных в базу.
- **fastapi**: Приложение FastAPI, предоставляющее API для работы с данными.
- **prometheus**: Сервис мониторинга для сбора метрик.
- **grafana**: Сервис визуализации для отображения метрик из Prometheus.
- **tests**: Сервис для запуска тестов и проверки работы API.

## Переменные окружения

В проекте используются следующие переменные окружения:

- **PostgreSQL**:
  - `POSTGRES_USER=myuser`
  - `POSTGRES_PASSWORD=mypassword`
  - `POSTGRES_DB=mydatabase`

- **FastAPI**:
  - `DATABASE_URL=postgresql://myuser:mypassword@db:5432/mydatabase`

- **Grafana**:
  - `GF_SECURITY_ADMIN_PASSWORD=secret`

## Описание маршрутов API

### `/prices`
- **GET** `/prices?ticker=btc_usd`
  - Возвращает список всех цен для указанного тикера.

### `/prices/latest`
- **GET** `/prices/latest?ticker=btc_usd`
  - Возвращает последние данные о цене для указанного тикера.

### `/prices/filter`
- **GET** `/prices/filter?ticker=btc_usd&start_date=1633046400&end_date=1633132800`
  - Возвращает отфильтрованные данные о ценах в указанном диапазоне дат.

### `/metrics`
- **GET** `/metrics`
  - Экспонирует метрики для Prometheus для мониторинга.

## Установка и запуск

### Шаг 1: Клонируйте репозиторий

```bash
git clone https://github.com/galetaa/Deribit-client
cd Deribit-client
```

### Шаг 2: Соберите и запустите контейнеры Docker

Для запуска всех сервисов выполните команду:

```bash
docker-compose up --build
```

Это запустит следующие контейнеры:
- **`db`**: База данных PostgreSQL
- **`client`**: Клиент для загрузки данных
- **`fastapi`**: Сервер FastAPI для API
- **`prometheus`**: Сервер Prometheus для мониторинга
- **`grafana`**: Сервер Grafana для визуализации метрик

### Шаг 3: Доступ к сервисам

- **FastAPI**: API доступно по адресу [http://localhost:8000](http://localhost:8000).
- **Prometheus**: Доступ к Prometheus можно получить по адресу [http://localhost:9090](http://localhost:9090).
- **Grafana**: Доступ к Grafana можно получить по адресу [http://localhost:3000](http://localhost:3000).
  - Логин по умолчанию: `admin`
  - Пароль: `secret`

### Шаг 4: Запуск тестов

Для запуска тестов в контейнере Docker выполните:

```bash
docker-compose run --rm tests
```

Это запустит все тесты, находящиеся в каталоге `tests/`.

## Мониторинг с использованием Prometheus и Grafana

- **Prometheus** собирает метрики с `/metrics` FastAPI.
- **Grafana** визуализирует метрики, что позволяет мониторить работу API в реальном времени.

Настройка мониторинга:
1. **Prometheus** автоматически начнет собирать данные с эндпоинта `/metrics` FastAPI, согласно конфигурации в `prometheus.yml`.
2. **Grafana** доступна по адресу [http://localhost:3000](http://localhost:3000). Настройте источник данных и дашборды для визуализации метрик Prometheus.

### Пример настройки Grafana

1. Войдите в Grafana по адресу [http://localhost:3000](http://localhost:3000).
2. Добавьте Prometheus как источник данных:
   - URL: `http://prometheus:9090`
3. Импортируйте или создайте дашборды для визуализации метрик (например, количества запросов к API).

## Пример `.env` файла (необязательно)

Вы можете создать файл `.env` в корневом каталоге со следующим содержимым для удобного управления переменными окружения:

```env
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
POSTGRES_DB=mydatabase
DATABASE_URL=postgresql://myuser:mypassword@db:5432/mydatabase
GF_SECURITY_ADMIN_PASSWORD=secret
```

Затем измените `docker-compose.yml` для использования этих переменных, добавив `${VARIABLE_NAME}`.

## Устранение неполадок

- **Проблемы с подключением к базе данных**: Убедитесь, что контейнер PostgreSQL запущен и доступен. Логи можно посмотреть с помощью `docker logs postgres_db`.
- **Логи сервисов**: Используйте `docker-compose logs <service_name>` для просмотра логов любого сервиса.
- **Конфликты портов**: Убедитесь, что порты 5432, 8000, 9090 и 3000 не заняты другими приложениями.


## Лицензия

Этот проект распространяется под лицензией MIT.
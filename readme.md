Приложение для парсинга логов nginx.

Формат логов настраивается в файле log_parser/data/re_model.txt

**Переменные окружения при старте ()**:
- API_HOST (по умолчанию 127.0.0.1)
- API_PORT (по умолчанию 8040)
- NGINX_FILE_PATH (путь к папке с логами)

**Запросы**
- GET запрос к /api/v1/get_metrics - получение данных по логам в формате:
  {
    "response_statuses": {
        "200": 26,
        "201": 4
    },
    "average_time": 122.333,
    "median_time": 99.5,
    "endpoints": {
        "/1/processing/feedback": 2,
        "/1/puller/tasks": 4,
        "/1/puller/sender": 4,
        "/api/v1/monitors/photos": 2,
        "/1/license?targets=expiration_time": 8,
        "/1/estimator": 2
    },
    "ips": {
        "10.1.41.23": 2,
        "10.1.41.24": 2,
        "10.1.41.13": 6,
        "127.0.0.1": 10,
        "10.1.41.11": 10
    },
    "methods": {
        "POST": 22,
        "GET": 8
    }
  }
- GET запрос к /version - получение версии приложения.
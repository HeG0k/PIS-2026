# Testing Strategy - Request Service

Примеры тестирования для **Request Service** (ПСО «Юго-Запад»).

---

## Структура

```
tests/
├── unit/
│   ├── domain/
│   │   ├── test_request_aggregate.py       # Инварианты, события
│   │   ├── test_group_entity.py
│   │   └── test_value_objects.py
│   └── application/
│       ├── test_create_request_handler.py  # Mock repository
│       └── test_query_handlers.py
├── integration/
│   ├── test_request_repository.py          # Testcontainers PostgreSQL
│   └── test_event_publisher.py             # RabbitMQ
├── e2e/
│   └── test_request_flow.py                # Полный сценарий API
└── conftest.py                             # Pytest fixtures
```

---

## Test Pyramid

```
      /\
     /E2E\        10% - E2E тесты (медленные, хрупкие)
    /------\
   /Integration\  20% - Интеграционные (БД, API)
  /--------------\
 /  Unit Tests   \ 70% - Юнит-тесты (быстрые, стабильные)
/------------------\
```

---

## Типы тестов

### 1. Юнит-тесты (Unit)

**Цель:** Проверить изолированную логику без внешних зависимостей.

**Что тестируем:**
- Domain Layer: инварианты, события, бизнес-правила
- Application Layer: handlers с mock-репозиториями

**Инструменты:**
- `pytest` - фреймворк
- `unittest.mock` - мокирование
- `pytest-cov` - покрытие

**Скорость:** 🚀 Очень быстро (миллисекунды)

---

### 2. Интеграционные тесты (Integration)

**Цель:** Проверить взаимодействие с внешними системами (БД, очереди).

**Что тестируем:**
- Repository ↔ PostgreSQL
- Event Publisher ↔ RabbitMQ
- REST Controller ↔ Handlers

**Инструменты:**
- `testcontainers` - реальная PostgreSQL в Docker
- `pytest-docker` - RabbitMQ в Docker

**Скорость:** 🐢 Медленно (секунды)

---

### 3. E2E-тесты (End-to-End)

**Цель:** Проверить полный сценарий через HTTP API.

**Что тестируем:**
- Полный flow: POST /requests → assign group → activate → GET /requests/{id}

**Инструменты:**
- `fastapi.testclient` - HTTP клиент
- `playwright` - браузерные тесты (опционально)

**Скорость:** 🐌 Очень медленно (десятки секунд)

---

## Примеры запуска

### Все тесты

```bash
pytest
```

### Только юнит-тесты

```bash
pytest tests/unit -v
```

### С покрытием

```bash
pytest --cov=domain --cov=application --cov-report=html
```

### Интеграционные (требуют Docker)

```bash
pytest tests/integration -v
```

### E2E

```bash
pytest tests/e2e -v --slow
```

---

## Покрытие кода

**Цель:** >= 90%

```bash
# Генерация отчёта
pytest --cov=. --cov-report=html

# Открыть отчёт
open htmlcov/index.html
```

---

## CI/CD (GitHub Actions)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v3
```

---

## Лучшие практики

### ✅ DO

- **Изолируйте тесты** - каждый тест независим
- **Используйте fixtures** - переиспользование setup/teardown
- **Называйте тесты говорящими именами** - `test_should_not_activate_without_group`
- **Тестируйте edge cases** - граничные значения, ошибки
- **Моките внешние зависимости** - в юнит-тестах

### ❌ DON'T

- **Не тестируйте фреймворк** - только свою логику
- **Не дублируйте тесты** - один тест на один сценарий
- **Не используйте production БД** - только testcontainers/in-memory
- **Не игнорируйте падающие тесты** - "flaky tests" = технический долг

---

## Mutation Testing (бонус)

**Цель:** Проверить качество тестов.

```bash
# Установка
pip install mutmut

# Запуск
mutmut run

# Результаты
mutmut show
```

**Ожидаемое:** >= 80% убитых мутантов.

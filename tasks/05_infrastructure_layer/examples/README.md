# Infrastructure Layer - Request Service

Примеры реализации инфраструктурного слоя для **Request Service** (ПСО «Юго-Запад»).

---

## Структура

```
infrastructure/
├── adapter/
│   ├── in/
│   │   └── request_controller.py        # FastAPI REST endpoints
│   └── out/
│       ├── request_repository_impl.py   # PostgreSQL через SQLAlchemy
│       └── event_publisher_impl.py      # RabbitMQ publisher
├── config/
│   └── database.py                      # DB connection pool
└── orm/
    └── models.py                        # SQLAlchemy ORM models
```

---

## Ключевые концепции

### Адаптеры (Adapters)

**Входящие адаптеры** (Driving Adapters):
- REST Controller - HTTP запросы → команды/запросы
- CLI - консольные команды

**Исходящие адаптеры** (Driven Adapters):
- Repository - доменные модели → БД
- Event Publisher - события → RabbitMQ/Kafka

### ORM vs Domain Model

**ORM Model** (SQLAlchemy):
- Аннотации БД (Column, ForeignKey)
- Flat structure (денормализация)

**Domain Model**:
- Бизнес-логика, инварианты
- Агрегаты, Value Objects

**Mapper** преобразует ORM ↔ Domain.

---

## Примеры использования

### 1. REST API (FastAPI)

```bash
# Создать заявку
curl -X POST http://localhost:8000/api/requests \
  -H "Content-Type: application/json" \
  -d '{
    "coordinator_id": "COORD-1",
    "zone_name": "North",
    "zone_bounds": [52.0, 52.5, 23.5, 24.0]
  }'

# Получить заявку
curl http://localhost:8000/api/requests/REQ-2024-0001
```

### 2. Repository (PostgreSQL)

```python
from infrastructure.adapter.out.request_repository_impl import RequestRepositoryImpl
from infrastructure.config.database import get_session

repo = RequestRepositoryImpl(get_session())

# Сохранить
repo.save(request)

# Найти
request = repo.find_by_id("REQ-2024-0001")
```

### 3. Docker Compose

```bash
# Запустить всю инфраструктуру
docker-compose up -d

# Проверить
docker-compose ps
```

---

## Миграции (Alembic)

```bash
# Создать миграцию
alembic revision --autogenerate -m "Create requests table"

# Применить
alembic upgrade head

# Откатить
alembic downgrade -1
```

---

## Связь с другими слоями

### Domain Layer (Lab #3)
- **Request** - агрегат, который сохраняется

### Application Layer (Lab #4)
- **CreateRequestHandler** → вызывает `repository.save()`
- **GetRequestByIdHandler** → вызывает `repository.find_by_id()`

### Infrastructure Layer (эта лаба)
- **RequestRepositoryImpl** - реализует интерфейс из Application
- **RequestController** - вызывает handlers

---

## Тестирование

### Интеграционные тесты (Testcontainers)

```python
from testcontainers.postgres import PostgresContainer

def test_repository_saves_request():
    with PostgresContainer("postgres:16") as postgres:
        # Arrange
        repo = RequestRepositoryImpl(postgres.get_connection_url())
        request = Request("REQ-2024-0001", "COORD-1", zone)
        
        # Act
        repo.save(request)
        
        # Assert
        found = repo.find_by_id("REQ-2024-0001")
        assert found.request_id == "REQ-2024-0001"
```

### E2E-тесты (FastAPI TestClient)

```python
from fastapi.testclient import TestClient

def test_create_request_via_api():
    client = TestClient(app)
    
    response = client.post("/api/requests", json={
        "coordinator_id": "COORD-1",
        "zone_name": "North",
        "zone_bounds": [52.0, 52.5, 23.5, 24.0]
    })
    
    assert response.status_code == 201
    assert "request_id" in response.json()
```

---

## Технологии

- **FastAPI** - REST API
- **SQLAlchemy** - ORM
- **Alembic** - миграции
- **PostgreSQL** - БД
- **Docker Compose** - оркестрация
- **Testcontainers** - тесты с реальной БД

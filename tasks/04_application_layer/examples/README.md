# Application Layer - Request Service

Примеры реализации прикладного слоя для **Request Service** (ПСО «Юго-Запад»).

---

## Структура

```
application/
├── command/
│   ├── create_request_command.py
│   ├── assign_group_command.py
│   └── handlers/
│       ├── create_request_handler.py
│       └── assign_group_handler.py
├── query/
│   ├── get_request_by_id_query.py
│   ├── dto/
│   │   └── request_dto.py       # Read-модель
│   └── handlers/
│       └── get_request_by_id_handler.py
└── service/
    └── request_service.py        # Фасад
```

---

## Ключевые концепции

### Command vs Query

| Aspect | Command | Query |
|--------|---------|-------|
| **Назначение** | Изменяет состояние | Читает данные |
| **Возвращает** | `None` или ID | DTO |
| **Пример** | CreateRequest | GetRequestById |

### Command Handler Pipeline

1. **Валидация** - проверка входных данных
2. **Загрузка** - получение агрегата из репозитория (если нужно)
3. **Выполнение** - вызов метода домена
4. **Сохранение** - запись изменений через Repository
5. **События** - публикация Domain Events

---

## Примеры использования

### Создание заявки

```python
from application.command.create_request_command import CreateRequestCommand
from application.command.handlers.create_request_handler import CreateRequestHandler

# Command
command = CreateRequestCommand(
    coordinator_id="COORD-1",
    zone_name="North",
    zone_bounds=(52.0, 52.5, 23.5, 24.0)
)

# Handler
handler = CreateRequestHandler(request_repository, event_publisher)
request_id = handler.handle(command)  # Возвращает "REQ-2024-0001"
```

### Получение заявки

```python
from application.query.get_request_by_id_query import GetRequestByIdQuery
from application.query.handlers.get_request_by_id_handler import GetRequestByIdHandler

# Query
query = GetRequestByIdQuery(request_id="REQ-2024-0001")

# Handler
handler = GetRequestByIdHandler(request_repository)
dto = handler.handle(query)  # Возвращает RequestDto
```

---

## Связь с частями системы

### Domain Layer (Lab #3)
- **Request** - aggregate root
- **Group**, **Zone** - доменные объекты
- **RequestStatus** - value object

### Infrastructure Layer (Lab #5)
- **RequestRepository** - реализация (PostgreSQL, in-memory)
- **EventBus** - публикация событий
- **REST Controller** - HTTP endpoints

---

## Тестирование

### Юнит-тесты Command Handler

```python
def test_create_request_handler():
    # Arrange
    mock_repo = Mock(RequestRepository)
    handler = CreateRequestHandler(mock_repo, Mock())
    
    command = CreateRequestCommand("COORD-1", "North", (52.0, 52.5, 23.5, 24.0))
    
    # Act
    request_id = handler.handle(command)
    
    # Assert
    assert request_id.startswith("REQ-")
    mock_repo.save.assert_called_once()
```

### Интеграционные тесты

```python
def test_create_request_via_service():
    # Arrange
    service = RequestService(...)
    
    command = CreateRequestCommand(...)
    
    # Act
    request_id = service.create_request(command)
    
    # Assert
    query = GetRequestByIdQuery(request_id)
    dto = service.get_request_by_id(query)
    
    assert dto.status == "DRAFT"
    assert dto.zone_name == "North"
```

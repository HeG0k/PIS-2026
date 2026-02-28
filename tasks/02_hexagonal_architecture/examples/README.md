# Примеры для Лабораторной работы №2

**Предметная область:** Поисково-спасательный отряд «Юго-Запад» (ПСО)

---

## 📋 Описание

Данный пример демонстрирует реализацию **Request Service** (Сервис управления заявками) с использованием гексагональной архитектуры для системы ПСО «Юго-Запад».

**Request Service** отвечает за:
- Создание заявки на поисково-спасательную операцию
- Формирование поисковой группы
- Уведомление участников через SMS
- Назначение зоны поиска

---

## 🏗️ Архитектура

### Слои системы

```
┌─────────────────────────────────────────┐
│   Infrastructure Layer                  │
│  ┌─────────────┐    ┌────────────────┐  │
│  │   REST      │    │   PostgreSQL   │  │
│  │ Controller  │    │   Repository   │  │
│  │   (HTTP)    │    │   (Adapter)    │  │
│  └──────┬──────┘    └────────┬───────┘  │
│         │                    │          │
│         │     ┌──────────────┴───┐      │
│         │     │  SMS Service     │      │
│         │     │  (Mock Adapter)  │      │
│         │     └──────────────────┘      │
└─────────┼────────────┬─────────────────┘
          │            │
          ▼            ▼
┌──────────────────────────────────────────┐
│   Application Layer                      │
│  ┌───────────────────────────────────┐   │
│  │         Ports (Interfaces)        │   │
│  │  ┌────────────┐  ┌─────────────┐  │   │
│  │  │  Inbound   │  │  Outbound   │  │   │
│  │  │   Ports    │  │   Ports     │  │   │
│  │  └─────┬──────┘  └──────┬──────┘  │   │
│  └────────┼─────────────────┼─────────┘   │
│           │                 │             │
│  ┌────────▼─────────────────▼─────────┐   │
│  │      RequestService                │   │
│  │  (implements CreateRequestUseCase) │   │
│  └────────────────────────────────────┘   │
└──────────────────┬───────────────────────┘
                   │
                   ▼
┌───────────────────────────────────────────┐
│       Domain Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │ Request  │  │  Group   │  │  Zone  │  │
│  │(Aggregate)│ │ (Entity) │  │  (VO)  │  │
│  └──────────┘  └──────────┘  └────────┘  │
│                                           │
│  Business Rules:                          │
│  - Request ID: REQ-YYYY-NNNN              │
│  - Group size: 3-5 participants           │
│  - Zone: North/South/East/West            │
│  - Status: DRAFT → ACTIVE → COMPLETED     │
└───────────────────────────────────────────┘
```

---

## 📦 Структура проекта

```
examples/
├── README.md                      # Этот файл (общее описание)
├── architecture-diagram.puml      # PlantUML диаграмма слоёв
└── src_python/                    # Python реализация
    ├── domain/                    # Domain Layer
    │   ├── request.py
    │   ├── group.py
    │   ├── zone.py
    │   └── request_status.py
    ├── application/               # Application Layer
    │   ├── port/
    │   │   ├── in/
    │   │   │   └── create_request_use_case.py
    │   │   └── out/
    │   │       ├── request_repository.py
    │   │       └── notification_service.py
    │   └── service/
    │       └── request_service.py
    ├── infrastructure/            # Infrastructure Layer
    │   ├── adapter/
    │   │   ├── in/
    │   │   │   └── request_controller.py  # FastAPI
    │   │   └── out/
    │   │       ├── in_memory_request_repository.py
    │   │       └── mock_sms_service.py
    │   └── config/
    │       └── dependency_injection.py
    ├── main.py                    # FastAPI приложение
    ├── example_cli.py             # CLI пример
    ├── requirements.txt           # Зависимости
    └── README.md                  # Детальная документация
```

---

## 🎯 Основные сущности из Lab #1

Данный пример использует те же сущности, что были описаны в [Lab #1](../../01_transaction_scenario/examples/):

### 1. Request (Заявка)

**Идентификатор:** REQ-2024-0042

**Атрибуты:**
- `id` - уникальный идентификатор (REQ-YYYY-NNNN)
- `coordinatorId` - ID координатора
- `zone` - зона поиска (Zone)
- `group` - поисковая группа (Group)
- `status` - статус (DRAFT, ACTIVE, COMPLETED)
- `createdAt` - дата создания

**Бизнес-правила:**
- Заявка создаётся в статусе DRAFT
- Группа формируется из 3-5 участников
- После формирования группы статус → ACTIVE
- Зона назначается координатором

### 2. Group (Группа)

**Идентификатор:** G-01

**Атрибуты:**
- `id` - уникальный идентификатор группы
- `members` - список участников (Volunteer)
- `leaderId` - ID лидера группы
- `zone` - назначенная зона

**Бизнес-правила:**
- Минимум 3 участника
- Максимум 5 участников
- Один участник назначается лидером

### 3. Zone (Зона поиска) - Value Object

**Возможные значения:**
- `NORTH` - Северная зона
- `SOUTH` - Южная зона
- `EAST` - Восточная зона
- `WEST` - Западная зона

**Свойства:**
- Immutable (неизменяемый)
- Equality by value (сравнение по значению)

---

## 🔌 Порты и адаптеры

### Входящие порты (Inbound Ports)

#### CreateRequestUseCase

Интерфейс для создания заявки:

```python
class CreateRequestUseCase(ABC):
    """Входящий порт для создания заявки"""
    
    @abstractmethod
    def create_request(self, command: CreateRequestCommand) -> str:
        """Создать заявку и вернуть её ID"""
        pass
```

**Command DTO:**
```python
@dataclass
class CreateRequestCommand:
    """Команда для создания заявки"""
    coordinator_id: str
    zone: str
    volunteer_ids: List[str]  # 3-5 участников
```

### Исходящие порты (Outbound Ports)
python
class RequestRepository(ABC):
    """Исходящий порт для работы с хранилищем"""
    
    @abstractmethod
    def save(self, request: Request) -> None:
        """Сохранить заявку"""
        pass
    
    @abstractmethod
    def find_by_id(self, request_id: str) -> Optional[Request]:
        """Найти заявку по ID"""
        pass
    
    @abstractmethod
    def find_by_status(self, status: RequestStatus) -> List[Request]:
        """Найти заявки по статусу"""
        pass
```

#### NotificationService

Интерфейс для уведомлений участников:

```python
class NotificationService(ABC):
    """Исходящий порт для отправки уведомлений"""
    
    @abstractmethod
    def send_sms(self, phone_number: str, message: str) -> None:
        """Отправить SMS"""
        pass
```

---

## 🎬 Сценарий работы (Use Case из Lab #1)

**Основной поток:**

1. **Координатор** создаёт заявку через REST API:
   ```bash
   POST /api/requests
   {
     "coordinatorId": "coordinator-001",
     "zone": "NORTH",
     "volunteerIds": ["vol-123", "vol-456", "vol-789"]
   }
   ```

2. **RequestController** (входящий адаптер) вызывает `CreateRequestUseCase`

3. **RequestService** (Application Layer):
   - Создаёт агрегат `Request` (Domain Layer)
   - Формирует `Group` с участниками
   - Назначает `Zone`
   - Сохраняет через `RequestRepository` (исходящий порт)
   - Отправляет SMS уведомления через `NotificationService` (исходящий порт)
-X POST http://localhost:8080/api/requests \
  -H "Content-Type: application/json" \
  -d '{
    "coordinatorId": "coordinator-001",
    "zone": "NORTH",
    "volunteerIds": ["vol-123", "vol-456", "vol-789"]
  }'

# Ответ:
# {
#   "requestId": "REQ-2024-0042"
# }
```

### Python версия

#### Установка зависимостей

```bash
# 1. Перейти в папку Python примера
cd examples/src_python

# 2. Создать виртуальное окружение
python -m venv venv

# 3. Активировать (Windows)
venv\Scripts\activate

# 3. Активировать (Linux/Mac)
source venv/bin/activate

# 4. Установить зависимости
pip install -r requirements.txt
```

### Вариант 1: CLI (без REST API)

```bash
python example_cli.py
```

**Вывод:**
```
============================================================
Request Service - ПСО «Юго-Запад»
Пример использования гексагональной архитектуры
============================================================

📋 Создание заявки...
   Координатор: coordinator-001
   Зона: NORTH
   Волонтёры: vol-123, vol-456, vol-789

✅ [Repository] Сохранена заявка: REQ-2024-0042
📱 [SMS] Кому: +375-29-XXX-0123
   Сообщение: Вы назначены в группу G-03 для поиска в зоне Северная зона
   ...

============================================================
✅ Заявка успешно создана!
   ID: REQ-2024-0042
============================================================
```

### Вариант 2: REST API (FastAPI)

```bash
# 1. Запустить FastAPI сервер
python main.py
```

Откроется на: http://localhost:8000

**Интерактивная документация API:** http://localhost:8000/docs

**Создать заявку через curl:**
```bash
curl -X POST http://localhost:8000/api/requests \
  -H "Content-Type: application/json" \
  -d '{
    "coordinator_id": "coordinator-001",
    "zone": "NORTH",
    "volunteer_ids": ["vol-123", "vol-456", "vol-789"]
  }'
```

**Ответ:**
```json
{
  "request_id": "REQ-2024-0042"
}
```

📖 **Подробнее:** см. [src_python/README.md](src_python/README.md)

---

## 🔍 Ключевые особенности гексагональной архитектуры

### 1. Dependency Inversion Principle (DIP)

**RequestService** зависит от **интерфейсов** (портов), а не от конкретных реализаций:

```python
class RequestService(CreateRequestUseCase):
    """Application Service реализует use-case"""
    
    def __init__(
        self,
        repository: RequestRepository,        # Интерфейс!
        notifications: NotificationService    # Интерфейс!
    ):
        self._repository = repository
        self._notifications = notifications
```

### 2. Тестируемость

Легко заменить реальные адаптеры на моки:

```python
def test_create_request():
    # Mock адаптеры
    mock_repo = Mock(spec=RequestRepository)
    mock_sms = Mock(spec=NotificationService)
    
    # Сервис с моками
    service = RequestService(mock_repo, mock_sms)
    
    # Тестируем бизнес-логику без БД и SMS
    command = CreateRequestCommand(...)
    request_id = service.create_request(command)
    
    # Проверки
    mock_repo.save.assert_called_once()
    assert mock_sms.send_sms.call_count == 3
```

### 3. Замена адаптеров без изменения бизнес-логики

**Было:** InMemoryRequestRepository  
**Стало:** PostgreSQLRequestRepository

**RequestService не изменился!** Только конфигурация DI:

```python
# В dependency_injection.py

# Было:
self._repository = InMemoryRequestRepository()

# Стало:
self._repository = PostgreSQLRequestRepository()
```

---

## 📚 Связь с Lab #1

| Элемент Lab #1 | Элемент Lab #2 | Описание |
|----------------|----------------|----------|
| Use-case "Создание заявки" | `CreateRequestUseCase` | Интерфейс для основного сценария |
| Сущность Request | `domain/request.py` | Агрегат с бизнес-правилами |
| Gherkin сценарий "Успешное создание" | `RequestService.createRequest()` | Реализация happy path |
| Транзакция "Сохранение + SMS" | `RequestRepository + NotificationService` | Разделение на порты |
| Sequence diagram | Architecture diagram | Визуализация взаимодействия слоёв |

---

## 💡 Что изучить дальше

- **Lab #3:** Domain Layer - подробная реализация агрегатов Request, Group, Zone
- **Lab #4:** Application Layer - CQRS разделение команд и запросов
- **Lab #5:** Infrastructure Layer - интеграция с PostgreSQL, RabbitMQ

---

## ❓ FAQ

**Q: Почему используются интерфейсы для портов, если реализация одна?**

A: Для тестируемости и возможности замены адаптера без изменения бизнес-логики. Сегодня InMemory, завтра PostgreSQL - `RequestService` не изменится.

**Q: Можно ли обойтись без плейсхолдеров в коде?**

A: Нет, это учебный пример. В production коде плейсхолдеры заменяются на реальные реализации.

**Q: Как связаны Request и Group?**

A: Request содержит Group как вложенный объект (композиция). При создании заявки формируется группа из указанных участников.

**Q: Почему Python, а не Java?**

A: Python выбран за лаконичность и простоту демонстрации архитектурных принципов:
- `abc.ABC` для портов (интерфейсов)
- `@dataclass` для DTO
- FastAPI для REST API с автодокументацией
- Простой DI без фреймворка

Принципы гексагональной архитектуры универсальны и применимы к любому языку!

**Q: Где посмотреть подробности реализации?**

A: См. [src_python/README.md](src_python/README.md) - детальное описание структуры, установки и запуска.

---

**Автор примера:** Базируется на предметной области ПСО «Юго-Запад» из Lab #1  
**Дата:** 18 февраля 2026

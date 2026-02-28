# Примеры для Лабораторной работы №3 - Domain Layer

**Предметная область:** Поисково-спасательный отряд «Юго-Запад» (ПСО)

---

## 📋 Описание

Этот пример демонстрирует **полноценную доменную модель** для Request Service из ПСО «Юго-Запад» с применением тактических паттернов DDD:
- **Entities** (Request, Group, Volunteer)
- **Value Objects** (Zone, PhoneNumber, RequestStatus)
- **Aggregate** (Request как корень)
- **Инварианты** (бизнес-правила)
- **Доменные события** (GroupAssignedToRequest, RequestActivated)

## 🔄 Связь с Lab #2

В Lab #2 мы создали **скелет** проекта с простыми классами:
```python
class Request:
    def __init__(self, request_id: str, ...):
        self.id = request_id
        # Минимум логики
```

В Lab #3 мы **наполняем** скелет полноценной бизнес-логикой:
```python
class Request:
    def assign_group(self, group: Group) -> None:
        # Валидация
        if self._status != RequestStatus.DRAFT:
            raise ValueError(...)
        
        # Инварианты
        if group.member_count < 3 or group.member_count > 5:
            raise ValueError(...)
        
        # Бизнес-логика
        self._assigned_group = group
        
        #  Доменное событие
        self._events.append(GroupAssignedToRequest(...))
```

## 📁 Структура примера

```
examples/
├── README.md                    # Этот файл
├── domain/                      # Domain Layer (полная реализация)
│   ├── models/
│   │   ├── request.py           # Aggregate Root с инвариантами
│   │   ├── group.py             # Entity
│   │   ├── volunteer.py         # Entity
│   │   ├── zone.py              # Value Object
│   │   ├── phone_number.py      # Value Object
│   │   └── request_status.py    # Enum Value Object
│   ├── events/
│   │   └── request_events.py    # Доменные события
│   └── exceptions/
│       └── domain_exceptions.py # Доменные исключения
└── tests/
    └── test_request.py          # Юнит-тесты инвариантов
```

## 🎯 Ключевые концепции

### 1. Entity vs Value Object

**Entity** (Request, Group, Volunteer):
- ✅ Имеет уникальный ID
- ✅ Равенство по ID
- ✅ Может изменяться (mutable)
- ✅ Бизнес-методы

**Value Object** (Zone, PhoneNumber):
- ✅ НЕТ ID (идентифицируется значениями)
- ✅ Равенство по всем полям
- ✅ Иммутабельный (frozen)
- ✅ Валидация в конструкторе

### 2. Aggregate Root (Request)

**Request** - корень агрегата:
- Единственная точка входа в агрегат
- Защищает инварианты (бизнес-правила)
- Регистрирует доменные события
- Управляет зависимыми сущностями (Group)

**Границы агрегата**:
- Внутри: Request (root) + assigned Group
- Снаружи: Volunteer, Coordinator (живут отдельно)

### 3. Инварианты (бизнес-правила)

| Инвариант | Где проверяется | Исключение |
|-----------|-----------------|------------|
| Группа 3-5 участников | `assign_group()` | ValueError |
| Нельзя назначить группу не в DRAFT | `assign_group()` | ValueError |
| Активировать только с группой | `activate()` | ValueError |
| Нельзя изменить завершённую заявку | `change_zone()` | ValueError |

### 4. Доменные события

События регистрируются при изменении состояния:
- `GroupAssignedToRequest` - когда группа назначена
- `RequestActivated` - когда операция начата
- `RequestZoneChanged` - когда зона изменена
- `RequestCompleted` - когда операция завершена

**Зачем нужны события?**
- Уведомления (отправить SMS участникам)
- Аудит (логировать историю изменений)
- Интеграция (запустить процесс в другом сервисе)
- Event Sourcing (восстановить состояние из событий)

## 🚀 Как использовать пример

### 1. Изучите доменные модели

Начните с простых Value Objects:
- [zone.py](domain/models/zone.py) - зона с координатами
- [phone_number.py](domain/models/phone_number.py) - телефон с валидацией

Затем Entity:
- [group.py](domain/models/group.py) - группа участников
- [volunteer.py](domain/models/volunteer.py) - волонтёр

И агрегат:
- [request.py](domain/models/request.py) - заявка (корень)

### 2. Изучите инварианты

Каждый бизнес-метод проверяет инварианты:
```python
def assign_group(self, group: Group) -> None:
    # Инвариант #1
    if self._status != RequestStatus.DRAFT:
        raise ValueError("Нельзя назначить группу...")
    
    # Инвариант #2
    if group.member_count < 3 or group.member_count > 5:
        raise ValueError("Группа должна содержать 3-5...")
```

### 3. Изучите доменные события

События создаются при важных изменениях:
```python
self._events.append(GroupAssignedToRequest(
    request_id=self._id,
    group_id=group.id,
    occurred_at=datetime.now()
))
```

### 4. Запустите тесты

```bash
cd examples/
pytest tests/
```

Тесты проверяют:
- ✅ Инварианты (нельзя нарушить бизнес-правила)
- ✅ Доменные события (регистрируются корректно)
- ✅ Value Objects (иммутабельность, валидация)

## 🔍 Отличия от Lab #2

| Аспект | Lab #2 (Скелет) | Lab #3 (Полная модель) |
|--------|-----------------|------------------------|
| Модели | Простые dataclasses | Богатая доменная модель |
| Бизнес-логика | Почти нет | Инварианты + валидация |
| События | Не реализованы | Полная реализация |
| Тесты | Не требуются | Юнит-тесты обязательны |
| Цель | Понять структуру | Реализовать логику |

## 💡 Советы по адаптации

Чтобы адаптировать пример под свою предметную область:

1. **Замените сущности:**
   - Request → Order/Booking/Task
   - Group → Team/OrderItems
   - Zone → Address/Category

2. **Определите свои инварианты:**
   - Какие бизнес-правила нельзя нарушить?
   - Когда выбрасывать исключения?

3. **Создайте свои события:**
   - Что важно для бизнеса?
   - Когда нужны уведомления?

4. **Напишите тесты:**
   - Каждый инвариант = минимум 1 тест
   - Проверяйте граничные условия

## 📚 Связь с другими лабами

- **Lab #1**: Use-cases "Создание заявки" → `Request.assign_group()`
- **Lab #2**: Скелет проекта → Теперь наполнен логикой
- **Lab #4**: Application Layer будет использовать эти модели
- **Lab #5**: Infrastructure сохранит Request в БД
- **Lab #6**: Тесты покроют весь стек
- **Lab #7**: Events → Event Bus → CQRS

## 🎓 Вопросы для самопроверки

1. Почему `Zone` - Value Object, а `Group` - Entity?
2. Можно ли изменить `PhoneNumber` после создания?
3. Что произойдёт если попытаться назначить группу с 2 участниками?
4. Зачем регистрировать событие `GroupAssignedToRequest`?
5. Где хранятся инварианты - в domain или application?

**Ответы в коде!** 😉

# Лабораторная работа №2. Гексагональная архитектура

**Дисциплина:** Проектирование интернет-систем  
**Тема:** Проектирование архитектуры: порты, адаптеры и изоляция домена

---

> 🚀 **Важно:** Эта лаба - про **архитектурное проектирование**, а не про глубокую реализацию. Создаём структуру проекта, интерфейсы портов и минимальные примеры каждого слоя. Детальное наполнение будет в Lab #3-5!

---

## Цель работы

Спроектировать архитектуру основного сервиса системы с использованием гексагональной (hexagonal) архитектуры: создать структуру проекта, определить порты (интерфейсы) и продемонстрировать изоляцию слоёв через минимальные примеры.

## Результаты обучения

После выполнения работы студент будет:
- Понимать принципы гексагональной архитектуры (Ports & Adapters)
- Уметь проектировать структуру проекта с разделением на слои: domain, application, infrastructure
- Определять порты (интерфейсы) для входящих и исходящих взаимодействий
- Применять Dependency Inversion Principle (DIP) на уровне проектирования
- Понимать как слои взаимодействуют через интерфейсы

## Теоретическая справка

### Гексагональная архитектура (Alistair Cockburn, 2005)

**Идея**: Бизнес-логика (домен) изолирована от внешнего мира через порты и адаптеры.

```
        ┌─────────────────────────┐
        │   Внешний мир           │
        │  (UI, БД, API, очереди) │
        └────────────┬────────────┘
                     │
            ┌────────▼────────┐
            │   Адаптеры      │ ◄─── Реализации (HTTP, PostgreSQL, RabbitMQ)
            │   (Infra Layer) │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │     Порты       │ ◄─── Интерфейсы (IOrderService, IRepository)
            │  (Application)  │
            └────────┬────────┘
                     │
            ┌────────▼────────┐
            │     Домен       │ ◄─── Чистая бизнес-логика (Order, Product)
            │  (Domain Layer) │
            └─────────────────┘
```

### Слои

1. **Domain** (ядро):
   - Сущности (Entities)
   - Value Objects
   - Доменная логика
   - **Не зависит** от фреймворков, БД, UI

2. **Application** (прикладной слой):
   - Use-case (сценарии)
   - Порты (интерфейсы):
     - **Входящие** (inbound): как внешний мир вызывает систему (`IOrderService`)
     - **Исходящие** (outbound): как система вызывает внешний мир (`IPaymentGateway`, `IRepository`)

3. **Infrastructure** (инфраструктурный):
   - Адаптеры:
     - **Входящие**: REST контроллеры, GraphQL resolvers, gRPC services
     - **Исходящие**: репозитории (БД), клиенты внешних API, очереди
   - Конфигурация, DI-контейнер

### Dependency Rule

**Зависимости направлены внутрь** (к домену):

```
Infrastructure → Application → Domain
     ↓                ↓            ↓
[Controllers]  →  [Ports]  →  [Entities]
[Repositories]
```

Domain **не знает** о Infrastructure!

## Задание

### Часть 1. Выбор центрального сервиса и создание архитектурной диаграммы

Выберите **один ключевой сервис** из вашей предметной области (из ЛР №1) и нарисуйте его архитектурную диаграмму.

Примеры сервисов:
- **Таск-трекер**: Task Service (управление задачами)
- **Бронь аудиторий**: Booking Service (бронирование слотов)
- **Мини-LMS**: Course Service (управление курсами)
- **Хэбит-трекер**: Habit Service (управление привычками)
- **Финучёт**: Transaction Service (управление транзакциями)

**Что нарисовать:**

1. **Диаграмму слоёв** (domain → application → infrastructure)
2. **Основные компоненты** каждого слоя:
   - Domain: 2-3 ключевые сущности (Task, Project, User)
   - Application: 2-3 use-case (CreateTask, AssignTask)
   - Infrastructure: входящие и исходящие адаптеры
3. **Потоки данных** (стрелки показывают направление вызовов)
4. **Зависимости** (подчеркнуть что domain НЕ зависит от infrastructure)

**Инструменты:** PlantUML, Draw.io, Mermaid, Excalidraw, или рисунок от руки

📖 **Пример диаграммы:** см. [examples/architecture-diagram.puml](examples/architecture-diagram.puml)

### Часть 2. Создание структуры проекта (скелет)

Создайте **скелет проекта** - структуру папок без детальной реализации:

```
your-service/
├── src/                                 # Исходный код
│   ├── domain/                          # Domain Layer
│   │   ├── models/                      # Доменные сущности (пока пустые классы)
│   │   │   ├── task.py                  # class Task: pass
│   │   │   ├── project.py               # class Project: pass
│   │   │   └── user.py                  # class User: pass
│   │   └── exceptions/
│   │       └── domain_exception.py      # class DomainException(Exception): pass
│   │
│   ├── application/                     # Application Layer
│   │   ├── port/
│   │   │   ├── in/                      # Входящие порты (интерфейсы use-cases)
│   │   │   │   ├── create_task_use_case.py    # Только интерфейс
│   │   │   │   └── get_task_use_case.py       # Только интерфейс
│   │   │   └── out/                     # Исходящие порты (интерфейсы зависимостей)
│   │   │       ├── task_repository.py         # Только интерфейс
│   │   │       └── notification_service.py    # Только интерфейс
│   │   └── service/
│   │       └── task_service.py          # Пустой класс с TODO-комментариями
│   │
│   └── infrastructure/                  # Infrastructure Layer
│       ├── adapter/
│       │   ├── in/
│       │   │   └── task_controller.py   # Один простой эндпоинт для демонстрации
│       │   └── out/
│       │       └── in_memory_task_repository.py  # Простая реализация
│       └── config/
│           └── dependency_injection.py  # Скелет DI-контейнера
│
├── README.md                            # Описание архитектуры вашего сервиса
└── Architecture.md                      # Диаграмма + объяснение портов
```

**Требования:**
- ✅ Все папки созданы
- ✅ Файлы созданы (могут быть пустыми или с минимальным кодом)
- ✅ Комментарии в файлах объясняют назначение
- ❌ НЕ требуется полная реализация (это будет в Lab #3-5)

📖 **Пример скелета:** см. [examples/src_python/](examples/src_python/)

### Часть 3. Определение интерфейсов портов

Создайте **интерфейсы** для входящих и исходящих портов (без реализации).

#### Входящие порты (что может делать клиент):

**CreateTaskUseCase** - интерфейс для создания задачи:
```python
# application/port/in/create_task_use_case.py
from abc import ABC, abstractmethod

class CreateTaskCommand:
    """DTO для команды создания задачи"""
    def __init__(self, title: str, description: str, assignee_id: str):
        self.title = title
        self.description = description
        self.assignee_id = assignee_id

class CreateTaskUseCase(ABC):
    """Входящий порт: создание задачи"""
    
    @abstractmethod
    def create_task(self, command: CreateTaskCommand) -> str:
        """
        Создаёт задачу и возвращает её ID
        :param command: Данные для создания
        :return: ID созданной задачи
        """
        pass
```

**GetTaskUseCase** - интерфейс для получения задачи:
```python
# application/port/in/get_task_use_case.py
from abc import ABC, abstractmethod

class GetTaskUseCase(ABC):
    """Входящий порт: получение задачи по ID"""
    
    @abstractmethod
    def get_task(self, task_id: str):
        """
        Получает задачу по ID
        :param task_id: Идентификатор задачи
        :return: Объект Task или None
        """
        pass
```

#### Исходящие порты (что нужно системе от внешнего мира):

**TaskRepository** - интерфейс для работы с БД:
```python
# application/port/out/task_repository.py
from abc import ABC, abstractmethod

class TaskRepository(ABC):
    """Исходящий порт: сохранение и загрузка задач"""
    
    @abstractmethod
    def save(self, task) -> None:
        """Сохраняет задачу"""
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: str):
        """Находит задачу по ID"""
        pass
```

**NotificationService** - интерфейс для уведомлений:
```python
# application/port/out/notification_service.py
from abc import ABC, abstractmethod

class NotificationService(ABC):
    """Исходящий порт: отправка уведомлений"""
    
    @abstractmethod
    def send_task_assigned(self, task_id: str, assignee_email: str) -> None:
        """Уведомляет исполнителя о назначении задачи"""
        pass
```

**Требования:**
- ✅ Все интерфейсы созданы
- ✅ Используется `ABC` и `@abstractmethod` (Python) или `interface` (Java/C#)
- ✅ Есть docstring/комментарии с назначением каждого метода
- ❌ НЕ требуется реализация (это будет в Lab #4)

📖 **Полные примеры:** см. [examples/src_python/application/port/](examples/src_python/application/port/)

### Часть 4. Создание минимальных примеров каждого слоя

Создайте **по одному простому примеру** для каждого слоя, чтобы продемонстрировать их взаимодействие.

#### Domain Layer - простая модель Task:

```python
# domain/models/task.py
class Task:
    """Доменная модель: Задача"""
    
    def __init__(self, task_id: str, title: str, description: str):
        self.id = task_id
        self.title = title
        self.description = description
        self.assignee_id = None
        self.status = "TODO"
    
    def assign(self, assignee_id: str):
        """Назначить исполнителя"""
        self.assignee_id = assignee_id
        # Полную бизнес-логику добавим в Lab #3
```

**Требования:**
- ✅ Простой класс с конструктором
- ✅ 1-2 метода для демонстрации
- ❌ НЕ требуется сложная бизнес-логика (это будет в Lab #3)

#### Application Layer - скелет сервиса:

```python
# application/service/task_service.py
class TaskService:
    """Реализация use-cases для управления задачами"""
    
    def __init__(self, repository, notification_service):
        self.repository = repository
        self.notification_service = notification_service
    
    def create_task(self, command):
        # TODO: реализовать в Lab #4
        # 1. Создать Task (domain)
        # 2. Сохранить через repository
        # 3. Вернуть ID
        raise NotImplementedError("Будет реализовано в Lab #4")
    
    def get_task(self, task_id: str):
        # TODO: реализовать в Lab #4
        raise NotImplementedError("Будет реализовано в Lab #4")
```

**Требования:**
- ✅ Конструктор принимает зависимости (порты)
- ✅ Методы объявлены с TODO-комментариями
- ❌ НЕ требуется полная реализация (это будет в Lab #4)

#### Infrastructure Layer - простой адаптер:

```python
# infrastructure/adapter/out/in_memory_task_repository.py
class InMemoryTaskRepository:
    """Реализация TaskRepository: хранение в памяти"""
    
    def __init__(self):
        self.tasks = {}  # Dict[str, Task]
    
    def save(self, task):
        self.tasks[task.id] = task
    
    def find_by_id(self, task_id: str):
        return self.tasks.get(task_id)
```

**Требования:**
- ✅ Простая реализация (словарь, список)
- ✅ Работает для демонстрации
- ❌ НЕ требуется БД (это будет в Lab #5)

### Часть 5. Конфигурация Dependency Injection (скелет)

Создайте **скелет** конфигурации для связывания компонентов:

```python
# infrastructure/config/dependency_injection.py
class DependencyContainer:
    """Конфигурация DI: связывание портов и адаптеров"""
    
    def __init__(self):
        # Создаём исходящие адаптеры
        self.task_repository = InMemoryTaskRepository()
        self.notification_service = ConsoleNotificationService()
        
        # Создаём application service с инжекцией зависимостей
        self.task_service = TaskService(
            repository=self.task_repository,
            notification_service=self.notification_service
        )
    
    def get_task_service(self):
        return self.task_service
```

**Ключевой принцип:** TaskService **не создаёт** зависимости сам - они передаются через конструктор!

📖 **Полный пример:** см. [examples/src_python/infrastructure/config/](examples/src_python/infrastructure/config/)

<!-- START:artifacts -->
## Структура отчёта

📄 **[Макет отчёта для заполнения →](Макет_отчета.md)**

Создайте в **своём репозитории** папку `lab-02/` со следующей структурой:

```
lab-02/
├── Отчет.md                # Заполненный макет отчёта
├── README.md               # Описание архитектуры вашего сервиса
├── Architecture.md         # Диаграмма слоёв + пояснения
└── src/                    # Скелет проекта
    ├── domain/
    │   └── models/         # Простые доменные классы
    ├── application/
    │   ├── port/
    │   │   ├── in/         # Интерфейсы входящих портов
    │   │   └── out/        # Интерфейсы исходящих портов
    │   └── service/        # Скелет сервиса с TODO
    └── infrastructure/
        ├── adapter/
        │   ├── in/         # Простой контроллер (опционально)
        │   └── out/        # Простой адаптер (InMemory)
        └── config/         # Скелет DI-контейнера
```

**Как заполнить отчёт:**
1. Скопируйте [Макет_отчета.md](Макет_отчета.md) в свой репозиторий как `Отчет.md`
2. Замените все плейсхолдеры (в `_[квадратных скобках]_`) на свои данные
3. Добавьте диаграмму архитектуры в `Architecture.md`
4. Опишите каждый порт (для чего, какие методы)
5. Покажите код интерфейсов портов
6. Напишите выводы о принципах гексагональной архитектуры
<!-- END:artifacts -->

<!-- START:criteria -->
## Критерии оценки

| Критерий | Баллы | Требования |
|----------|-------|------------|
| Архитектурная диаграмма | 25 | Ясная диаграмма слоёв с компонентами и зависимостями |
| Структура проекта (скелет) | 20 | Корректное разделение на domain/application/infrastructure, все папки созданы |
| Интерфейсы портов | 30 | Входящие (2+) и исходящие (2+) порты определены корректно, с документацией |
| Простые примеры слоёв | 15 | По одному простому примеру каждого слоя (domain, application, infrastructure) |
| DI конфигурация (скелет) | 5 | Скелет контейнера демонстрирует принцип инжекции зависимостей |
| Качество документации | 5 | README и Architecture.md объясняют архитектуру, назначение портов, принцип DIP |
| **ИТОГО** | **100** | |
<!-- END:criteria -->

<!-- START:bonuses -->
## Бонусы (+ до 15)

* **Диаграмма в PlantUML с C4 Model** (+5) - использование C4 диаграммы (Context, Container, Component) вместо простой схемы слоёв
* **Альтернативная архитектурная диаграмма** (+4) - дополнительная диаграмма последовательности (sequence diagram), показывающая поток вызовов через порты
* **Документация принципов SOLID** (+3) - раздел в Architecture.md с объяснением как каждый принцип SOLID применён в архитектуре
* **Сравнение с Layered Architecture** (+3) - диаграмма и текст, сравнивающие hexagonal и классическую трёхслойную архитектуру
<!-- END:bonuses -->

## Контрольные вопросы для защиты

1. В чём преимущество гексагональной архитектуры перед трёхслойной architecture)?
2. Почему domain не должен зависеть от infrastructure?
3. Что такое Dependency Inversion Principle? Как он применяется в гексагональной архитектуре?
4. Зачем создавать интерфейсы для портов, если пока у них только одна реализация?
5. Как изменится архитектура при переходе с REST на gRPC? Какие слои затронуты?
6. В чём разница между входящим и исходящим портом? Приведите примеры.
7. Почему domain-сущности не должны иметь аннотаций фреймворков (@Entity, @Table)?
8. Как обеспечивается тестируемость в гексагональной архитектуре?
9. Можно ли заменить InMemoryRepository на PostgreSQLRepository без изменения domain и application слоёв? Почему?
10. В какой слой поместить валидацию входных данных? В domain, application или infrastructure?

## Полезные ресурсы

### 📖 Документация и примеры
- **[Макет отчёта](Макет_отчета.md)** - шаблон для заполнения
- **Примеры структуры проекта** - см. раздел "Часть 2" выше

### 🔗 Внешние ресурсы
- [Alistair Cockburn: Hexagonal Architecture](https://alistair.cockburn.us/hexagonal-architecture/) - оригинальная статья автора паттерна
- [Netflix: Ready for changes with Hexagonal Architecture](https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749) - опыт Netflix
- [Get Your Hands Dirty on Clean Architecture (book)](https://www.packtpub.com/product/get-your-hands-dirty-on-clean-architecture/9781839211966) - практическое руководство
- [Martin Fowler: Dependency Injection](https://martinfowler.com/articles/injection.html) - про DI принцип
- [Uncle Bob: Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - фундаментальная статья

## Срок сдачи

**Неделя 4-5 семестра**  
Защита: демонстрация диаграммы, структуры проекта, интерфейсов портов + ответы на контрольные вопросы

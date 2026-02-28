# Microservices Architecture - Request & Group Services

Примеры реализации **микросервисной архитектуры** для ПСО «Юго-Запад».

---

## Архитектура системы

```
┌─────────────────────────────────────────────────────────────┐
│                        API Gateway                          │
│                     (nginx / Kong)                          │
└───────────────────┬────────────────────┬───────────────────┘
                    │                    │
        ┌───────────▼──────────┐    ┌───▼──────────────────┐
        │ Request Service      │    │ Group Service         │
        │ (FastAPI)            │    │ (FastAPI)             │
        │                      │    │                       │
        │ - Create Request     │    │ - Create Group        │
        │ - Assign Group       │    │ - Mark Ready          │
        │ - Activate Request   │    │ - Assign to Request   │
        └──────────┬───────────┘    └──────────┬────────────┘
                   │                           │
                   │  Events (RabbitMQ)        │
                   │  ┌──────────────────┐     │
                   └──►  RequestCreated  ◄─────┘
                      │  GroupReady      │
                      │  GroupAssigned   │
                      └──────────────────┘
                   │                           │
        ┌──────────▼───────────┐    ┌─────────▼─────────────┐
        │ PostgreSQL           │    │ PostgreSQL            │
        │ (requests_db)        │    │ (groups_db)           │
        └──────────────────────┘    └───────────────────────┘
```

---

## Bounded Contexts

### Request Service (Bounded Context #1)

**Ответственность:** Управление заявками

**Сущности:**
- Request (aggregate root)
- Zone (value object)
- Coordinator (reference)

**События:**
- `RequestCreated` → уведомить Group Service
- `RequestActivated` → уведомить UI
- `RequestCompleted` → уведомить Statistics Service

**API:**
- `POST /requests` - создать заявку
- `GET /requests/{id}` - получить заявку
- `PUT /requests/{id}/activate` - активировать заявку

**База данных:** `requests_db` (PostgreSQL)

---

### Group Service (Bounded Context #2)

**Ответственность:** Управление группами волонтёров

**Сущности:**
- Group (aggregate root)
- Volunteer (entity)
- Equipment (value object)

**События:**
- `GroupCreated` → регистрация группы
- `GroupReady` → можно назначить на заявку
- `GroupAssignedToRequest` → группа занята

**API:**
- `POST /groups` - создать группу
- `GET /groups/{id}` - получить группу
- `PUT /groups/{id}/mark-ready` - отметить готовность

**База данных:** `groups_db` (PostgreSQL)

---

## Event-Driven Communication

### Схема взаимодействия

```
Request Service                RabbitMQ               Group Service
───────────────────────────────────────────────────────────────────

1. POST /requests
   ↓
2. Create Request
   ↓
3. Publish(RequestCreated) ───────→  [Event Bus]
                                         │
                                         └──────→  4. Subscribe
                                                      ↓
                                                   5. Find ready Group
                                                      ↓
                                                   6. Publish(GroupReady)
                                         ┌──────────┘
                                         │
7. Subscribe ←───────────────────────   [Event Bus]
   ↓
8. Assign Group to Request
   ↓
9. Publish(GroupAssigned) ────────→  [Event Bus]
                                         │
                                         └──────→ 10. Mark Group as BUSY
```

---

## Структура проекта

```
microservices/
├── request-service/
│   ├── main.py                  # FastAPI app
│   ├── domain/
│   │   └── request.py
│   ├── application/
│   │   └── handlers/
│   ├── infrastructure/
│   │   ├── repository/
│   │   ├── event_bus/
│   │   │   └── rabbitmq_publisher.py
│   │   └── api/
│   ├── Dockerfile
│   └── requirements.txt
│
├── group-service/
│   ├── main.py
│   ├── domain/
│   │   └── group.py
│   ├── infrastructure/
│   │   └── event_bus/
│   │       └── rabbitmq_subscriber.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── api-gateway/
│   └── nginx.conf
│
└── docker-compose.yml
```

---

## RabbitMQ Event Bus

### Publisher (Request Service)

```python
import pika
import json

class RabbitMQPublisher:
    def __init__(self, host='rabbitmq'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='pso_events', exchange_type='topic')
    
    def publish(self, event_type: str, payload: dict):
        self.channel.basic_publish(
            exchange='pso_events',
            routing_key=event_type,
            body=json.dumps(payload)
        )
        print(f"📤 Event published: {event_type}")
```

### Subscriber (Group Service)

```python
import pika
import json

class RabbitMQSubscriber:
    def __init__(self, host='rabbitmq'):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host)
        )
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='pso_events', exchange_type='topic')
        
        # Очередь для Group Service
        result = self.channel.queue_declare(queue='group_service_queue', durable=True)
        self.channel.queue_bind(
            exchange='pso_events',
            queue='group_service_queue',
            routing_key='RequestCreated'
        )
    
    def subscribe(self, callback):
        self.channel.basic_consume(
            queue='group_service_queue',
            on_message_callback=callback,
            auto_ack=True
        )
        print('📥 Listening for events...')
        self.channel.start_consuming()
```

---

## API Gateway (nginx)

### nginx.conf

```nginx
upstream request_service {
    server request-service:8001;
}

upstream group_service {
    server group-service:8002;
}

server {
    listen 80;
    
    # Request Service routes
    location /requests {
        proxy_pass http://request_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Group Service routes
    location /groups {
        proxy_pass http://group_service;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    # Health check
    location /health {
        return 200 "OK";
    }
}
```

---

## docker-compose.yml

```yaml
version: '3.8'

services:
  # Request Service
  request-service:
    build: ./request-service
    ports:
      - "8001:8000"
    environment:
      DATABASE_URL: postgresql://user:password@requests-db:5432/requests
      RABBITMQ_HOST: rabbitmq
    depends_on:
      - requests-db
      - rabbitmq
  
  # Group Service
  group-service:
    build: ./group-service
    ports:
      - "8002:8000"
    environment:
      DATABASE_URL: postgresql://user:password@groups-db:5432/groups
      RABBITMQ_HOST: rabbitmq
    depends_on:
      - groups-db
      - rabbitmq
  
  # Databases
  requests-db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: requests
    volumes:
      - requests-data:/var/lib/postgresql/data
  
  groups-db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: groups
    volumes:
      - groups-data:/var/lib/postgresql/data
  
  # Message Broker
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: password
  
  # API Gateway
  api-gateway:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./api-gateway/nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - request-service
      - group-service

volumes:
  requests-data:
  groups-data:
```

---

## Паттерны микросервисов

### 1. Database per Service

**Принцип:** Каждый сервис имеет свою БД

**Преимущества:**
- Независимость развёртывания
- Выбор технологии БД под задачу
- Изоляция данных

**Недостатки:**
- Нет транзакций между сервисами
- Дублирование данных

### 2. Event-Driven Communication

**Принцип:** Сервисы общаются через события

**Преимущества:**
- Слабая связанность (loose coupling)
- Асинхронность
- Масштабируемость

**Недостатки:**
- Eventual Consistency
- Сложность отладки

### 3. API Gateway

**Принцип:** Единая точка входа для клиентов

**Преимущества:**
- Скрывает внутреннюю архитектуру
- Централизованная аутентификация
- Rate limiting, CORS

**Недостатки:**
- Single Point of Failure
- Bottleneck

### 4. Circuit Breaker

**Принцип:** Предотвращение каскадных сбоев

```python
from pybreaker import CircuitBreaker

breaker = CircuitBreaker(fail_max=5, timeout_duration=60)

@breaker
def call_group_service(group_id: str):
    response = requests.get(f"http://group-service/groups/{group_id}")
    return response.json()
```

---

## Service Discovery

### Consul (пример)

```python
import consul

# Регистрация Request Service
c = consul.Consul()
c.agent.service.register(
    name='request-service',
    service_id='request-service-1',
    address='request-service',
    port=8000,
    check=consul.Check.http('http://request-service:8000/health', interval='10s')
)

# Поиск Group Service
services = c.catalog.service('group-service')
group_service_url = f"http://{services[0]['ServiceAddress']}:{services[0]['ServicePort']}"
```

---

## Преимущества микросервисов

✅ **Независимое развёртывание** - Request Service можно деплоить отдельно  
✅ **Масштабируемость** - можно масштабировать только Group Service  
✅ **Технологическая гибкость** - Request Service на Python, Group Service на Go  
✅ **Изоляция сбоев** - падение Group Service не ломает Request Service

---

## Недостатки микросервисов

❌ **Сложность** - вместо 1 приложения теперь 3+ сервиса  
❌ **Распределённые транзакции** - Saga, 2PC  
❌ **Мониторинг** - нужен Prometheus, Grafana, Jaeger  
❌ **Тестирование** - E2E тесты сложнее

---

## Запуск

```bash
# Сборка и запуск
docker-compose up --build

# Проверка сервисов
curl http://localhost/requests
curl http://localhost/groups

# RabbitMQ Management UI
open http://localhost:15672  # admin:password
```

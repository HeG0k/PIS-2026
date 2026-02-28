# Лабораторная работа №9. Protocol Buffers и gRPC (Высокопроизводительное RPC)

**Дисциплина:** Проектирование интернет-систем  
**Тема:** gRPC, Protocol Buffers, streaming

---

## Цель работы

Заменить REST API на **gRPC** для межсервисной коммуникации:
- **Схемы** - `.proto` файлы
- **Server/Client** - gRPC реализация
- **Streaming** - real-time обновления

---

## Результаты обучения

- **Определять** service-контракты в `.proto`
- **Генерировать** код из протофайлов
- **Реализовывать** unary/streaming RPC
- **Сравнивать** gRPC и REST

---

## Задание

### Часть 1. Протофайлы (.proto)

**Определение сервисов и сообщений:**

📖 **Пример:** [examples/proto/request_service.proto](examples/proto/request_service.proto)

```protobuf
syntax = "proto3";

service RequestService {
  rpc CreateRequest(CreateRequestRequest) returns (CreateRequestResponse);
  rpc GetRequest(GetRequestRequest) returns (RequestDto);
}

message CreateRequestRequest {
  string coordinator_id = 1;
  string zone_name = 2;
  // ...
}
```

---

### Часть 2. gRPC Server

**Реализация сервиса:**

📖 **Пример:** [examples/server/request_service_server.py](examples/server/request_service_server.py)

---

### Часть 3. gRPC Client

**Вызов удалённых методов:**

📖 **Пример:** [examples/client/request_service_client.py](examples/client/request_service_client.py)

---

### Часть 4. Streaming

**Server-side streaming для обновлений:**

📖 **Пример:** Реализовано в [examples/server/request_service_server.py](examples/server/request_service_server.py) (метод `StreamActiveRequests`)

---

<!-- START:artifacts -->
## Структура отчёта

📄 **[Макет отчёта →](Макет_отчета.md)**

```
lab-09/
├── Отчет.md
├── proto/
│   └── request_service.proto
├── grpc/
│   ├── server.py
│   └── client.py
└── tests/
    └── test_grpc.py
```
<!-- END:artifacts -->

<!-- START:criteria -->
## Критерии оценки

| Критерий | Баллы | Требования |
|----------|-------|------------|
| Протофайлы: схемы сервисов | 20 | .proto с комментариями |
| gRPC Server: реализация сервисов | 25 | CreateRequest, GetRequest |
| gRPC Client: вызовы RPC | 20 | Тесты клиента |
| Streaming: server-side streaming | 20 | Real-time обновления |
| Генерация кода: protoc | 10 | Автоматическая генерация |
| Качество документации | 5 | README, примеры |
| **ИТОГО** | **100** | |
<!-- END:criteria -->

<!-- START:bonuses -->
## Бонусы (+ до 15)

* **Bidirectional Streaming** (+5) - двусторонний поток
* **Interceptors** (+4) - аутентификация, логирование
* **gRPC-Web** (+3) - gRPC из браузера
* **Load Balancing** (+3) - клиентский балансировщик
<!-- END:bonuses -->

## Контрольные вопросы

1. **В чём преимущество gRPC над REST?**
2. **Почему Protocol Buffers быстрее JSON?**
3. **Зачем нужен streaming в gRPC?**
4. **Когда использовать REST, а когда gRPC?**

---

## Срок сдачи

**Неделя 18-19 семестра**  
Защита: демонстрация работы gRPC + streaming

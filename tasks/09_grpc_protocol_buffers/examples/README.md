# gRPC & Protocol Buffers - Request Service

Примеры реализации **gRPC API** для Request Service (ПСО «Юго-Запад»).

---

## Зачем gRPC?

### REST API (HTTP/JSON)

```
Client                          Server
  │                                │
  │─── GET /requests/REQ-001 ─────>│
  │                                │
  │<─── 200 OK (JSON 250 bytes) ───│
```

**Размер:** ~250 байт  
**Парсинг:** JSON → Python dict (медленно)  
**Типы:** Нет (всё строки/числа)

---

### gRPC (HTTP/2 + Protobuf)

```
Client                          Server
  │                                │
  │─── GetRequest(id="REQ-001") ──>│
  │                                │
  │<─── Request (binary 80 bytes) ─│
```

**Размер:** ~80 байт (в 3 раза меньше)  
**Парсинг:** Protobuf → Python object (быстро)  
**Типы:** Строгая типизация (схема .proto)

---

## Преимущества gRPC

✅ **Производительность** - в 3-10 раз быстрее REST  
✅ **HTTP/2** - мультиплексирование, server push  
✅ **Streaming** - server/client/bidirectional streaming  
✅ **Строгая типизация** - схема .proto как контракт  
✅ **Code generation** - автогенерация клиентов (Python, Go, Java, C#)

---

## Структура проекта

```
grpc/
├── proto/
│   └── request_service.proto        # Protocol Buffers схема
├── generated/
│   ├── request_service_pb2.py       # Сгенерированные классы
│   └── request_service_pb2_grpc.py  # Сгенерированные стабы
├── server/
│   └── request_service_server.py    # gRPC Server
├── client/
│   └── request_service_client.py    # gRPC Client
└── requirements.txt
```

---

## Protocol Buffers Schema

### request_service.proto

```protobuf
syntax = "proto3";

package pso;

// ========================================
// Messages (Data Models)
// ========================================

message Zone {
  string name = 1;
  float lat_min = 2;
  float lat_max = 3;
  float lon_min = 4;
  float lon_max = 5;
}

message Request {
  string request_id = 1;
  string coordinator_id = 2;
  Zone zone = 3;
  string status = 4;  // "DRAFT", "ACTIVE", "COMPLETED"
  string assigned_group_id = 5;
  int64 created_at = 6;  // Unix timestamp
  int64 activated_at = 7;
  int64 completed_at = 8;
}

// ========================================
// Request/Response Messages
// ========================================

message CreateRequestRequest {
  string coordinator_id = 1;
  Zone zone = 2;
}

message CreateRequestResponse {
  string request_id = 1;
  string status = 2;  // "SUCCESS", "ERROR"
  string error_message = 3;
}

message GetRequestRequest {
  string request_id = 1;
}

message GetRequestResponse {
  Request request = 1;
  bool found = 2;
}

message StreamActiveRequestsRequest {
  // Пустой запрос (можно добавить фильтры)
}

// ========================================
// Service Definition
// ========================================

service RequestService {
  // Unary RPC: Create Request
  rpc CreateRequest(CreateRequestRequest) returns (CreateRequestResponse);
  
  // Unary RPC: Get Request by ID
  rpc GetRequest(GetRequestRequest) returns (GetRequestResponse);
  
  // Server-side Streaming: Stream active requests
  rpc StreamActiveRequests(StreamActiveRequestsRequest) returns (stream Request);
}
```

---

## Генерация кода

```bash
# Установка grpcio-tools
pip install grpcio-tools

# Генерация Python кода из .proto
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/request_service.proto

# Сгенерированные файлы:
# - request_service_pb2.py (классы Request, Zone, etc.)
# - request_service_pb2_grpc.py (RequestServiceServicer, Stub)
```

---

## gRPC Server

### request_service_server.py

```python
import grpc
from concurrent import futures
import time
from generated import request_service_pb2, request_service_pb2_grpc

class RequestServiceServicer(request_service_pb2_grpc.RequestServiceServicer):
    """
    gRPC Server: Request Service
    """
    
    def __init__(self):
        # In-memory storage (в реальности: PostgreSQL)
        self.requests = {}
    
    def CreateRequest(self, request, context):
        """Unary RPC: Create Request"""
        request_id = f"REQ-{int(time.time())}"
        
        # Создание Request
        new_request = request_service_pb2.Request(
            request_id=request_id,
            coordinator_id=request.coordinator_id,
            zone=request.zone,
            status="DRAFT",
            created_at=int(time.time())
        )
        
        self.requests[request_id] = new_request
        
        return request_service_pb2.CreateRequestResponse(
            request_id=request_id,
            status="SUCCESS"
        )
    
    def GetRequest(self, request, context):
        """Unary RPC: Get Request"""
        req = self.requests.get(request.request_id)
        
        if req:
            return request_service_pb2.GetRequestResponse(
                request=req,
                found=True
            )
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Request not found")
            return request_service_pb2.GetRequestResponse(found=False)
    
    def StreamActiveRequests(self, request, context):
        """Server-side Streaming: Stream active requests"""
        for req in self.requests.values():
            if req.status == "ACTIVE":
                yield req
                time.sleep(0.5)  # Имитация потока данных

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    request_service_pb2_grpc.add_RequestServiceServicer_to_server(
        RequestServiceServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🚀 gRPC Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

---

## gRPC Client

### request_service_client.py

```python
import grpc
from generated import request_service_pb2, request_service_pb2_grpc

def create_request(stub):
    """Unary RPC: Create Request"""
    zone = request_service_pb2.Zone(
        name="North",
        lat_min=52.0,
        lat_max=52.5,
        lon_min=23.5,
        lon_max=24.0
    )
    
    request = request_service_pb2.CreateRequestRequest(
        coordinator_id="COORD-1",
        zone=zone
    )
    
    response = stub.CreateRequest(request)
    print(f"✅ Request created: {response.request_id}")
    return response.request_id

def get_request(stub, request_id):
    """Unary RPC: Get Request"""
    request = request_service_pb2.GetRequestRequest(request_id=request_id)
    response = stub.GetRequest(request)
    
    if response.found:
        print(f"📦 Request: {response.request.request_id}")
        print(f"   Coordinator: {response.request.coordinator_id}")
        print(f"   Zone: {response.request.zone.name}")
        print(f"   Status: {response.request.status}")
    else:
        print("❌ Request not found")

def stream_active_requests(stub):
    """Server-side Streaming"""
    request = request_service_pb2.StreamActiveRequestsRequest()
    
    print("📡 Streaming active requests...")
    for req in stub.StreamActiveRequests(request):
        print(f"  → {req.request_id} ({req.status})")

def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = request_service_pb2_grpc.RequestServiceStub(channel)
        
        # 1. Create Request
        request_id = create_request(stub)
        
        # 2. Get Request
        get_request(stub, request_id)
        
        # 3. Stream active requests
        # stream_active_requests(stub)

if __name__ == '__main__':
    run()
```

---

## Типы RPC

### 1. Unary RPC (Request → Response)

```protobuf
rpc GetRequest(GetRequestRequest) returns (GetRequestResponse);
```

**Когда использовать:** CRUD операции (GET, POST, PUT, DELETE)

---

### 2. Server-side Streaming (Request → Stream)

```protobuf
rpc StreamActiveRequests(StreamActiveRequestsRequest) returns (stream Request);
```

**Когда использовать:** Длинные списки, live updates, мониторинг

**Пример:** Стрим активных заявок каждые 5 секунд

---

### 3. Client-side Streaming (Stream → Response)

```protobuf
rpc UploadZoneCoordinates(stream ZonePoint) returns (UploadResponse);
```

**Когда использовать:** Загрузка больших файлов, массовая вставка

---

### 4. Bidirectional Streaming (Stream ↔ Stream)

```protobuf
rpc ChatWithCoordinator(stream Message) returns (stream Message);
```

**Когда использовать:** Чаты, WebSocket-подобная коммуникация

---

## Запуск

```bash
# 1. Установка зависимостей
pip install grpcio grpcio-tools

# 2. Генерация кода из .proto
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/request_service.proto

# 3. Запуск сервера
python server/request_service_server.py

# 4. Запуск клиента (в другом терминале)
python client/request_service_client.py
```

---

## REST vs gRPC: Сравнение

| Критерий | REST API | gRPC |
|----------|----------|------|
| Протокол | HTTP/1.1 | HTTP/2 |
| Формат | JSON | Protobuf (binary) |
| Размер | ~250 bytes | ~80 bytes |
| Скорость | 100 RPS | 1000 RPS |
| Типизация | Нет | Строгая (.proto) |
| Streaming | WebSocket | Встроенный |
| Browser | ✅ Да | ❌ Нет (только через grpc-web) |
| Читаемость | ✅ JSON легко читать | ❌ Binary |

---

## Когда использовать gRPC?

### ✅ Используйте gRPC:

- **Микросервисы** - сервис-to-сервис коммуникация
- **Высокая нагрузка** - 10k+ RPS
- **Real-time** - streaming данных
- **Polyglot** - клиенты на разных языках (Python, Go, Java)

### ❌ Не используйте gRPC:

- **Browser** - нужен grpc-web (сложнее)
- **Публичное API** - REST понятнее для сторонних разработчиков
- **Отладка** - JSON легче читать в логах

---

## Дополнительные ресурсы

- **Официальная документация:** https://grpc.io/docs/languages/python/
- **Protocol Buffers:** https://protobuf.dev/
- **gRPC vs REST:** https://cloud.google.com/blog/products/api-management/understanding-grpc-openapi-and-rest

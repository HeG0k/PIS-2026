# gRPC Examples - Быстрый старт

## 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

## 2. Генерация кода из .proto

```bash
python -m grpc_tools.protoc \
  -I./proto \
  --python_out=./generated \
  --grpc_python_out=./generated \
  ./proto/request_service.proto
```

**Для Windows (PowerShell):**
```powershell
python -m grpc_tools.protoc `
  -I./proto `
  --python_out=./generated `
  --grpc_python_out=./generated `
  ./proto/request_service.proto
```

Сгенерированные файлы:
- `generated/request_service_pb2.py` - классы Request, Zone, CreateRequestRequest, etc.
- `generated/request_service_pb2_grpc.py` - RequestServiceServicer, RequestServiceStub

## 3. Запуск сервера

```bash
# В терминале #1
python server/request_service_server.py
```

Вывод:
```
🚀 gRPC Server started on port 50051
📡 Listening for requests...
```

## 4. Запуск клиента

```bash
# В терминале #2
python client/request_service_client.py
```

Вывод:
```
=== CreateRequest ===
✅ Request created: REQ-2024-0004

=== GetRequest(REQ-2024-0004) ===
📦 Request ID: REQ-2024-0004
   Coordinator: COORD-1
   Zone: North (52.0, 52.5)
   Status: DRAFT
   Created: 1717777777

=== ActivateRequest(REQ-2024-0004) ===
🚀 Request activated: REQ-2024-0004

=== ListRequests(filter=ALL) ===
📋 Found 4 requests:
  → REQ-2024-0001 (ACTIVE) - North
  → REQ-2024-0002 (ACTIVE) - South
  → REQ-2024-0003 (COMPLETED) - East
  → REQ-2024-0004 (ACTIVE) - North

=== ListRequests(filter=ACTIVE) ===
📋 Found 3 requests:
  → REQ-2024-0001 (ACTIVE) - North
  → REQ-2024-0002 (ACTIVE) - South
  → REQ-2024-0004 (ACTIVE) - North
```

## 5. Тестирование Streaming

Раскомментируйте строку в `client/request_service_client.py`:

```python
# 6. Стрим активных заявок
stream_active_requests(stub)
```

Запустите клиента снова:

```bash
python client/request_service_client.py
```

Вывод (в real-time):
```
=== StreamActiveRequests ===
📡 Streaming active requests (press Ctrl+C to stop)...
  → REQ-2024-0001 (ACTIVE) - Zone: North
  → REQ-2024-0002 (ACTIVE) - Zone: South
  → REQ-2024-0004 (ACTIVE) - Zone: North
  [пауза 2 секунды]
  → REQ-2024-0001 (ACTIVE) - Zone: North
  → REQ-2024-0002 (ACTIVE) - Zone: South
  ...
```

Нажмите `Ctrl+C` для остановки стрима.

## Структура проекта

```
examples/
├── proto/
│   └── request_service.proto        # Protocol Buffers схема
├── generated/                        # Сгенерированные файлы (создаются автоматически)
│   ├── request_service_pb2.py
│   └── request_service_pb2_grpc.py
├── server/
│   └── request_service_server.py    # gRPC Server
├── client/
│   └── request_service_client.py    # gRPC Client
├── requirements.txt
└── QUICK_START.md                   # Этот файл
```

## Частые проблемы

### Проблема: `ModuleNotFoundError: No module named 'generated'`

**Решение:**
```bash
# Убедитесь, что вы сгенерировали код из .proto
python -m grpc_tools.protoc -I./proto --python_out=./generated --grpc_python_out=./generated ./proto/request_service.proto

# Проверьте, что файлы созданы
ls generated/
```

### Проблема: `grpc._channel._InactiveRpcError: <_InactiveRpcError of RPC that terminated with: status = UNAVAILABLE`

**Решение:** Сервер не запущен. Запустите сервер в отдельном терминале:
```bash
python server/request_service_server.py
```

### Проблема: `SyntaxError` в сгенерированных файлах

**Решение:** Проверьте версию protobuf:
```bash
pip install --upgrade protobuf==4.25.3
```

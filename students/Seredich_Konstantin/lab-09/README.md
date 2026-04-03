# Лабораторная №9 — gRPC / Protocol Buffers

## Зависимости

```bash
py -m pip install -r requirements.txt
```

## Генерация кода из `.proto`

После изменения [proto/request_service.proto](proto/request_service.proto):

```bash
py -m grpc_tools.protoc -I proto --python_out=generated --grpc_python_out=generated proto/request_service.proto
```

В каталоге `generated/` появятся `request_service_pb2.py` и `request_service_pb2_grpc.py`.

## Запуск сервера и клиента

```bash
py grpc/server.py
```

В другом терминале:

```bash
py grpc/client.py
```

## Тесты

```bash
py -m pytest tests -v
```
